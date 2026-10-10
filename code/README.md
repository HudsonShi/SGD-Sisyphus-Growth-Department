# code/ —— 配套示例脚本

这些脚本是《增长技术笔记》正文的**可运行配套代码**，用来把公式变成肌肉记忆。
全部只依赖 Python 3 标准库（无需 pip install），直接 `python3 xxx.py` 即可运行。

```bash
cd code
python3 bm25_retrieval.py
python3 itemcf_recall.py
python3 metrics_auc_gauc.py
python3 ab_test_planner.py
python3 crossborder_unit_economics.py
```

| 脚本 | 对应章节 | 用途 | 关键公式/方法 |
|---|---|---|---|
| `bm25_retrieval.py` | ch01 / ch07 | 从零实现倒排索引 + Okapi BM25 检索（中文字符 bigram 分词） | BM25 打分、IDF、词频饱和 $k_1$、长度归一化 $b$ |
| `itemcf_recall.py` | ch03 | 从零实现 ItemCF 召回：共现统计 → 相似度 → 截断 → 多路加权聚合 | 余弦相似度、热门惩罚、时间衰减 |
| `metrics_auc_gauc.py` | ch01 / ch02 | AUC（秩和法，含并列处理）、GAUC、NDCG@K、MRR、Recall@K、LogLoss | Mann-Whitney U、分组 AUC、DCG/IDCG |
| `ab_test_planner.py` | ch21 | 样本量 / MDE / 实验时长计算，CUPED 方差缩减收益估算 | 两比例样本量公式、Acklam 逆正态近似、$\theta=\mathrm{Cov}(X,Y)/\mathrm{Var}(X)$ |
| `crossborder_unit_economics.py` | ch18 / ch20 | 跨境单位经济模型（落地成本、盈亏平衡价、最大可承受 CPA）+ 安全库存 / ROP / EOQ | 落地成本、$SS=z\sqrt{LT\sigma_d^2+d^2\sigma_{LT}^2}$、$EOQ=\sqrt{2DS/H}$ |
| `funnel_analysis.sql` | ch01 / ch21 | 全链路漏斗、分渠道 UV 价值、留存曲线、多渠道归因对账、素材疲劳监测 | 条件聚合、窗口函数、FULL OUTER JOIN 对账 |

---

## 几个提醒

1. **这些脚本里的数字都是演示量级**，不是任何真实公司的数据。
   真实投放/核算请以平台后台与财务口径为准。
2. `funnel_analysis.sql` 里的表名（`dwd_event`、`dwd_order`、`ods_google_ads_daily` 等）
   是**假设的数仓表结构**，需要替换成你自己的表。
   日期函数也需要按引擎调整（Presto 用 `date_add`，BigQuery 用 `DATE_ADD`，ClickHouse 用 `addDays`）。
3. 想要更接近生产的实现，可以看这些库：
   - 检索：`rank_bm25`、`pyserini`、`faiss`、`hnswlib`、`sentence-transformers`
   - 推荐：`implicit`（ALS/BPR）、`LightFM`、`RecBole`、`TorchRec`
   - 指标：`scikit-learn`（`roc_auc_score`、`ndcg_score`）、`torchmetrics`
   - 实验：`statsmodels`（`power`）、`scipy.stats`、`CausalPy`

---

## 练习建议

学完对应章节后，试着**故意改坏**这些脚本，观察指标怎么变——这比读十遍公式有用：

- 把 `bm25_retrieval.py` 的 `K1` 改成 0.1 和 10，看词频饱和的效果；
  把 `B` 改成 0 和 1，看长度惩罚的效果。
- 把 `itemcf_recall.py` 的热门惩罚指数从 0.5 改成 0，观察头部商品如何淹没推荐结果。
- 把 `metrics_auc_gauc.py` 里 demo 第二段的组间偏移从 3.0 改成 0，看 AUC 与 GAUC 如何趋于一致。
- 把 `ab_test_planner.py` 的基线 CVR 从 3% 改成 0.3%，感受样本量如何随转化率急剧膨胀。
- 把 `crossborder_unit_economics.py` 的 `return_rate` 从 8% 拉到 25%，看利润如何被退货吃掉。
