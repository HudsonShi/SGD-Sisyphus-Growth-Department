-- ===========================================================================
-- funnel_analysis.sql
-- Companion SQL for <<Growth Tech Notes>> ch21 (Growth Loop) and ch01 (funnel).
--
-- Dialect: ANSI-ish, tested mentally against Presto/Trino, Hive, BigQuery,
--          ClickHouse and DuckDB. Adjust date functions per engine.
--
-- Tables assumed:
--   dwd_event        (dt, user_id, session_id, event, item_id, price, channel, utm_source, utm_campaign)
--   dwd_order        (dt, order_id, user_id, session_id, gmv, refund_amount, channel)
--   dim_channel      (channel, channel_type, is_paid, platform)
-- ===========================================================================


-- ---------------------------------------------------------------------------
-- 1. 全链路漏斗：曝光 -> 点击 -> 详情 -> 加购 -> 结账 -> 支付
--    用条件聚合一次算出每层 UV 与相邻层的转化率。
-- ---------------------------------------------------------------------------
WITH funnel AS (
    SELECT
        dt,
        COUNT(DISTINCT CASE WHEN event = 'impression'   THEN user_id END) AS uv_impression,
        COUNT(DISTINCT CASE WHEN event = 'click'        THEN user_id END) AS uv_click,
        COUNT(DISTINCT CASE WHEN event = 'view_detail'  THEN user_id END) AS uv_detail,
        COUNT(DISTINCT CASE WHEN event = 'add_cart'     THEN user_id END) AS uv_cart,
        COUNT(DISTINCT CASE WHEN event = 'begin_checkout' THEN user_id END) AS uv_checkout,
        COUNT(DISTINCT CASE WHEN event = 'purchase'     THEN user_id END) AS uv_purchase
    FROM dwd_event
    WHERE dt BETWEEN DATE '2024-01-01' AND DATE '2024-01-31'
    GROUP BY dt
)
SELECT
    dt,
    uv_impression,
    uv_click,
    ROUND(1.0 * uv_click    / NULLIF(uv_impression, 0), 4) AS ctr,
    ROUND(1.0 * uv_detail   / NULLIF(uv_click, 0), 4)      AS click_to_detail,
    ROUND(1.0 * uv_cart     / NULLIF(uv_detail, 0), 4)     AS detail_to_cart,
    ROUND(1.0 * uv_checkout / NULLIF(uv_cart, 0), 4)       AS cart_to_checkout,
    ROUND(1.0 * uv_purchase / NULLIF(uv_checkout, 0), 4)   AS checkout_to_pay,
    -- overall conversion, the multiplicative chain in one number
    ROUND(1.0 * uv_purchase / NULLIF(uv_impression, 0), 4) AS impression_to_pay
FROM funnel
ORDER BY dt;


-- ---------------------------------------------------------------------------
-- 2. 分渠道漏斗 + 单位经济：哪个渠道的 UV 价值最高？
--    UV 价值 = 渠道 GMV / 渠道 UV，比 ROAS 更能暴露"高客单低转化"的渠道。
-- ---------------------------------------------------------------------------
WITH channel_traffic AS (
    SELECT
        utm_source AS channel,
        COUNT(DISTINCT user_id) AS uv
    FROM dwd_event
    WHERE dt BETWEEN DATE '2024-01-01' AND DATE '2024-01-31'
      AND event = 'session_start'
    GROUP BY utm_source
),
channel_revenue AS (
    SELECT
        e.utm_source AS channel,
        SUM(o.gmv)                    AS gmv,
        SUM(o.refund_amount)          AS refund,
        COUNT(DISTINCT o.order_id)    AS orders,
        1.0 * SUM(o.gmv) / NULLIF(COUNT(DISTINCT o.order_id), 0) AS aov
    FROM dwd_order o
    JOIN (SELECT DISTINCT user_id, session_id, utm_source FROM dwd_event) e
      ON o.user_id = e.user_id AND o.session_id = e.session_id
    WHERE o.dt BETWEEN DATE '2024-01-01' AND DATE '2024-01-31'
    GROUP BY e.utm_source
)
SELECT
    t.channel,
    d.channel_type,
    d.is_paid,
    t.uv,
    r.orders,
    ROUND(1.0 * r.orders / NULLIF(t.uv, 0), 4)        AS cvr,
    ROUND(r.gmv, 2)                                    AS gmv,
    ROUND(r.gmv - COALESCE(r.refund, 0), 2)            AS net_gmv,
    ROUND(r.aov, 2)                                    AS aov,
    ROUND((r.gmv - COALESCE(r.refund, 0)) / NULLIF(t.uv, 0), 4) AS gmv_per_uv,
    ROUND(COALESCE(r.refund, 0) / NULLIF(r.gmv, 0), 4) AS refund_rate
FROM channel_traffic t
LEFT JOIN channel_revenue r ON t.channel = r.channel
LEFT JOIN dim_channel d     ON t.channel = d.channel
ORDER BY gmv_per_uv DESC NULLS LAST;


-- ---------------------------------------------------------------------------
-- 3. 留存曲线（次日/7 日/30 日），用于 LTV 与 CAC 的回本判断。
-- ---------------------------------------------------------------------------
WITH first_seen AS (
    SELECT user_id, MIN(dt) AS first_dt
    FROM dwd_event
    WHERE event = 'purchase'
    GROUP BY user_id
),
activity AS (
    SELECT DISTINCT e.user_id, e.dt
    FROM dwd_event e
    WHERE e.event = 'purchase'
)
SELECT
    f.first_dt,
    COUNT(DISTINCT f.user_id) AS cohort_size,
    COUNT(DISTINCT CASE WHEN a.dt = f.first_dt + INTERVAL '1'  DAY THEN a.user_id END) AS d1,
    COUNT(DISTINCT CASE WHEN a.dt = f.first_dt + INTERVAL '7'  DAY THEN a.user_id END) AS d7,
    COUNT(DISTINCT CASE WHEN a.dt = f.first_dt + INTERVAL '30' DAY THEN a.user_id END) AS d30,
    ROUND(1.0 * COUNT(DISTINCT CASE WHEN a.dt = f.first_dt + INTERVAL '7' DAY
              THEN a.user_id END) / NULLIF(COUNT(DISTINCT f.user_id), 0), 4) AS retention_d7
FROM first_seen f
LEFT JOIN activity a ON f.user_id = a.user_id
GROUP BY f.first_dt
ORDER BY f.first_dt;


-- ---------------------------------------------------------------------------
-- 4. 多渠道对账表：平台后台 vs 站内埋点 vs 实际订单
--    这是发现"平台归因虚高"的第一步。
-- ---------------------------------------------------------------------------
WITH platform_reported AS (
    -- 从各平台后台导出后 union 成一张表
    SELECT 'google_ads'   AS platform, dt, conversions, cost FROM ods_google_ads_daily
    UNION ALL
    SELECT 'meta_ads',     dt, conversions, cost FROM ods_meta_ads_daily
    UNION ALL
    SELECT 'tiktok_ads',   dt, conversions, cost FROM ods_tiktok_ads_daily
),
site_reported AS (
    SELECT
        utm_source AS platform,
        dt,
        COUNT(DISTINCT order_id) AS orders,
        SUM(gmv)                 AS gmv
    FROM dwd_order
    GROUP BY utm_source, dt
)
SELECT
    p.platform,
    p.dt,
    p.conversions        AS platform_conversions,
    s.orders             AS site_orders,
    ROUND(1.0 * p.conversions / NULLIF(s.orders, 0), 3)                 AS platform_over_site,
    ROUND(p.cost, 2)                                                    AS cost,
    ROUND(s.gmv, 2)                                                     AS gmv,
    ROUND(s.gmv / NULLIF(p.cost, 0), 2)                                 AS roas,
    ROUND(p.cost / NULLIF(p.conversions, 0), 2)                         AS cpa_reported
FROM platform_reported p
FULL OUTER JOIN site_reported s
  ON p.platform = s.platform AND p.dt = s.dt
ORDER BY p.dt DESC, cost DESC;


-- ---------------------------------------------------------------------------
-- 5. 素材疲劳监测：同一素材 Frequency 与 CTR 的 7 日滑窗
-- ---------------------------------------------------------------------------
SELECT
    creative_id,
    dt,
    SUM(impressions) AS impressions,
    SUM(clicks)      AS clicks,
    ROUND(1.0 * SUM(clicks) / NULLIF(SUM(impressions), 0), 5) AS ctr,
    ROUND(1.0 * SUM(impressions) / NULLIF(SUM(reach), 0), 2)  AS frequency,
    -- 7-day moving CTR, used as the fatigue baseline
    ROUND(AVG(1.0 * clicks / NULLIF(impressions, 0)) OVER (
        PARTITION BY creative_id ORDER BY dt
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW), 5) AS ctr_ma7
FROM dwd_ad_daily
GROUP BY creative_id, dt
HAVING SUM(impressions) > 1000
ORDER BY creative_id, dt;
