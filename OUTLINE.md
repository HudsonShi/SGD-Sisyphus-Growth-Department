# 全书详细大纲（OUTLINE）

> 写作时**严格按本大纲的小节标题组织**，可以增加小节，但不要遗漏本大纲列出的要点。
> 目标：内容尽可能丰富、有信息量、有工程细节、有取舍分析。

---

## 第 1 部分 基础：从流量到增长的全景

### ch01 导论：从信息检索到增长工程 ✅（已完成，见 chapters/ch01-overview.tex，作为文风范本）

### ch02 数学、统计与工程基础（chapters/ch02-math-foundations.tex，`ch:math`）
- **开篇洞察**：算法工程师真正每天用到的数学是什么？
- 线性代数与向量检索基础：内积/余弦/欧氏距离的关系、矩阵分解的几何直觉、SVD、PCA、双塔为何用内积、
  归一化与否对检索的影响、量化（PQ/SQ）的数学原理。
- 概率与统计：条件概率与贝叶斯、极大似然、指数族与 logistic 的联系、偏差-方差分解、
  假设检验（t 检验、卡方、bootstrap）、置信区间、多重比较与 FDR、功效分析（power/sample size）。
- 优化：凸与非凸、梯度下降家族（SGD/Momentum/AdaGrad/Adam）、牛顿法与拟牛顿、
  正则化（L1/L2/弹性网）、拉格朗日乘子与 KKT（用于预算约束）、
  FTRL-Proximal 的推导直觉与稀疏性优势、采样 softmax 与负采样。
- 机器学习基础：偏差-方差、过拟合与正则、树模型（GBDT/XGBoost/LightGBM）原理、
  特征重要性与 SHAP、类别特征处理（one-hot/target encoding/embedding/哈希）、
  特征穿越（feature leakage）与时间旅行问题、样本权重与校准（Platt scaling / isotonic）。
- 评估指标大全：分类（AUC/GAUC/LogLoss/PR-AUC/校准度）、
  排序（NDCG/MRR/MAP/Recall@K/HitRate/GAUC 的分组含义）、
  回归（RMSE/MAE/MAPE）、业务（ROI/ROAS/LTV/CAC/ARPU/留存曲线）。
  **给出 AUC 的概率解释与 GAUC 公式**。
- 工程基础：分布式训练（数据并行/模型并行/参数服务器/AllReduce）、
  混合精度、Embedding 表的显存估算公式、批推理与 GPU 利用率、
  在线服务延迟预算拆解（p99 的构成）、缓存与降级策略。
- 数据基础：数仓分层（ODS/DWD/DWS/ADS）、离线/近线/实时三条链路、
  Lambda vs Kappa 架构、流批一体、样本回填与特征一致性。
- **实操盒**：Embedding 显存与 QPS 估算表；一份「模型上线前的 20 项检查清单」。
- **陷阱盒**：离线 AUC 涨但线上不涨（呼应 ch01）；特征穿越的五种典型形态。
- **面试题**：AUC 的计算与物理意义？为什么用 GAUC？FTRL 为什么稀疏？

---

## 第 2 部分 推荐算法

### ch03 推荐系统总论与召回（chapters/ch03-recsys-recall.tex，`ch:recall`）
- **开篇洞察**：推荐系统的本质是「信息过载下的效用最大化」，召回决定了效果上限。
- 推荐问题形式化：用户-物品交互矩阵、显式 vs 隐式反馈、评分预测 vs Top-N 推荐的目标差异。
- 协同过滤：UserCF/ItemCF 原理与公式（相似度、共现、归一化）、
  ItemCF 为什么在工业界优于 UserCF（物品稳定性、可解释、离线可算）、
  Swing 算法与热门惩罚、i2i 的召回与截断、相似度计算的工程实现（倒排 + 多路合并）。
- 矩阵分解：FunkSVD、SVD++、BPR 的 pairwise 损失推导、ALS 与 SGD 的取舍、隐式反馈加权（confidence）。
- 因子分解机与特征化召回：FM 公式推导（二阶交叉的线性复杂度）、FFM、Field 概念。
- 向量化召回（双塔）：YouTube DNN 的架构细节（样本构造、负采样、sampled softmax、
  用户塔/物品塔的输入特征、上线时用最近邻检索）、
  双塔的结构性缺陷（用户-物品交叉信息丢失）与改进（
  双塔 + 内积 vs 后期交互、多兴趣 MIND、TDM 树召回、深度树）。
- 图召回：ItemCF 的图上解释、随机游走（PersonalRank）、
  GraphSAGE/PinSage 的邻居采样与聚合、LightGCN 的简化、图召回的工程落地。
- 多路召回融合：并行召回池、分数归一化（min-max/rank/温度）、
  配额分配、以及「召回多样性 vs 精度」的权衡。
- 冷启动：内容侧特征、类目先验、Explore-Exploit（epsilon-greedy/UCB/Thompson）、
  新用户三档策略。
- **案例盒**：YouTube 双塔 / 阿里 TDM / Pinterest PinSage（三个案例选二展开）。
- **陷阱盒**：向量检索的「召回率幻觉」——ANN 索引参数、归一化、量化误差导致离线评估与线上不一致。
- **实操盒**：ItemCF 的 SQL/Python 实现思路；双塔负采样比例实验设计。
- **面试题**：ItemCF 与 UserCF 的区别与适用场景？双塔模型为什么不能做交叉特征？

### ch04 排序模型：从 LR 到多任务学习（chapters/ch04-recsys-ranking.tex，`ch:ranking`）
- **开篇洞察**：精排是「用算力换效果」的主战场，但收益边际递减，工程一致性往往比结构更重要。
- 逻辑回归时代：LR + 特征工程、FB 的 GBDT+LR（特征组合自动化）、
  为什么 GBDT+LR 在当年有效（树做非线性交叉 + LR 做校准）。
- 因子分解机家族：FM → FFM → AFM → DeepFM → xDeepFM → DCN/DCNv2，
  讲清「显式交叉 vs 隐式交叉」「低秩假设的代价」。
- 深度模型：Wide&Deep 的 Memorization + Generalization 框架、
  DeepFM 的共享 Embedding、DIN 的注意力机制（Activation Unit）、
  DIEN 的兴趣演化（GRU + AUGRU）、DSIN 的会话划分、
  BST 的 Transformer 化、AutoInt、FiBiNET。
- 多任务学习：Shared-Bottom 的跷跷板现象、MMoE 的门控机制、
  PLE 的 CGC 结构与任务隔离、ESSM 的全空间建模、
  以及「样本空间 vs 模型结构」两种解决多目标冲突的路线。
- 多目标融合：加权求和、乘性融合、排序学习（LTR）、
  约束优化与帕累托前沿、业务权重的手工调参问题。
- 位置偏差与消偏：PAL（Position-Aware Learning）的推导、
  训练加位置特征 + 服务置零的原理、以及为什么它能同时学位置与相关性。
- 校准与一致性：pCTR 校准（分桶校准/保序回归）、
  粗排与精排的一致性（蒸馏、全链路 LTR）。
- 损失函数与训练技巧：LogLoss vs Focal Loss vs 对比学习，
  多值特征、序列特征、实时特征的处理，样本加权与课程学习。
- **案例盒**：阿里 DIN/DIEN 系列演进；腾讯 PLE 的落地经验。
- **陷阱盒**：Embedding 维度爆炸与 OOV；模型越大线上越差的三种原因（延迟、特征不一致、过拟合）。
- **实操盒**：一份「精排上线 checklist」+ 特征重要度分析流程。
- **面试题**：DIN 相比 DeepFM 的改进？MMoE 与 PLE 的区别？如何做多目标融合？

### ch05 序列建模与生成式推荐（chapters/ch05-recsys-sequence-generative.tex，`ch:sequence`）
- **开篇洞察**：推荐正在从「排序一个静态候选集」走向「生成用户的下一步行为」。
- 序列推荐基础：会话 vs 长序列、GRU4Rec 的 session 建模、样本构造（滑窗）。
- 自注意力序列模型：SASRec（因果掩码、位置编码）、
  BERT4Rec（双向 + Cloze 目标，为什么能 work）、
  BST/S³-Rec/CL4SRec 的对比学习思路。
- 长序列建模：SIM（两阶段检索兴趣）、ETA、TWIN、
  长序列的工程挑战（存储、检索成本、训练稳定性）。
- 生成式推荐：TIGER（语义 ID + 生成式检索）、
  HSTU（Actions Speak Louder than Words，万亿参数序列 transducer、
  把推荐转成生成问题）、LLM4Rec 的三条路线（
  作为推荐器 / 作为特征增强 / 作为推理与解释器）。
- 语义 ID 与向量量化：RQ-VAE、层次 K-means、语义 ID 的构造与冲突处理。
- 强化学习与长期价值：MDP 建模、状态/动作/奖励设计、
  离线 RL（BCQ/CQL）在推荐中的尝试、为什么工业界落地困难。
- 扩散模型与其他生成范式在推荐中的探索。
- **案例盒**：HSTU 的实验结论与 Meta 的规模化经验；TIGER 的 semantic ID 效果。
- **陷阱盒**：「生成式推荐适合所有场景」的误解——候选集受限、可解释性、实时性、成本。
- **实操盒**：序列特征落地的数据模型设计（行为序列表、时间衰减、去重与截断策略）。
- **面试题**：SASRec 与 BERT4Rec 的区别？生成式推荐与双塔召回的优劣？

### ch06 推荐系统工程化（chapters/ch06-recsys-engineering.tex，`ch:receng`）
- **开篇洞察**：算法效果 = 模型能力 × 工程一致性，后者往往是瓶颈。
- 整体架构：召回-粗排-精排-重排-混排-策略层，各层 QPS/延迟/算力预算分配。
- 特征平台：离线特征（天级/小时级）、近线特征（流式计算）、
  实时特征（用户侧实时行为、上下文）、
  特征一致性校验（离线/在线 diff 工具）、特征血缘与版本管理。
- 样本工程：样本拼接（join 的时序正确性）、负采样策略、
  样本去重与比例控制、延迟反馈（delayed feedback）处理、
  位置偏差数据的采集（随机探索位）。
- 在线服务：预估服务架构（GPU 推理、批处理 trick、动态 batching）、
  模型热更新与灰度、A/B 分流与互斥层、
  全链路超时与降级（兜底策略、缓存、保底结果）。
- 训练系统：增量训练 vs 全量训练、在线学习（Online Learning）、
  流式样本与模型更新的延迟链路、灾难性遗忘与回滚。
- 实验平台：分流算法（哈希、一致性哈希、分层正交）、
  实验灵敏度（CUPED 方差缩减）、
  A/A 校验、多重比较、长期效应与 holdback。
- 生态与体验：内容多样性、作者生态、信息茧房度量、
  推荐系统的负反馈与用户控制。
- **案例盒**：某类电商推荐链路的延迟预算表（示范量级）。
- **陷阱盒**：离线训练与在线服务特征不一致的六种典型场景与排查方法。
- **实操盒**：推荐系统监控看板应包含的 20 个指标。
- **面试题**：如何保证离线在线一致性？如何设计一次推荐 A/B 实验？

---

## 第 3 部分 搜索引擎与自然语言处理

### ch07 搜索引擎原理与实现（chapters/ch07-search-engine.tex，`ch:search`）
- **开篇洞察**：搜索的每一步都是在「理解意图」与「匹配供给」之间做取舍。
- 整体架构：爬虫 → 解析 → 索引 → 检索 → 排序 → 展现；离线与在线链路。
- 索引：正排/倒排、词典与 posting list、跳表与压缩（VByte/PForDelta）、
  位置索引与短语查询、动态索引（全量 + 增量）、索引分片与副本。
- 检索模型：布尔模型、VSM、BM25（含公式与参数）、
  语言模型（Query Likelihood、Dirichlet 平滑）、
  LTR 三阶段（pointwise/pairwise/listwise）、
  LambdaMART 的 lambda 梯度直觉。
- 查询理解：分词（中文分词算法与词典、新词发现）、
  拼写纠错（编辑距离、噪声信道、n-gram 语言模型）、
  同义词与改写（query rewriting）、
  意图识别与 query 分类（导航/信息/交易）、
  查询扩展（伪相关反馈 RM3）、实体识别与知识图谱挂载。
- 召回与排序：多路召回（term match / 语义 / 图谱 / 个性化）、
  粗排（双塔 + 轻量特征）、精排（BERT 类交叉编码器的成本）、
  重排与结果聚合（多文档摘要、聚合卡片、电商的 SPU 聚合）。
- 垂直与电商搜索：类目预测、属性抽取、同款比价、
  商品标题的分词与权重、销量/评分/价格如何进入排序、无结果（zero-result）处理。
- 评价体系：离线（标注相关性、nDCG、MAP）、
  在线（CTR、长点击、跳出、无结果率、query 满意度、会话级指标）、
  人工评估与 LLM-as-judge 的可靠性与偏差。
- **案例盒**：电商搜索的类目预测与同款聚合（示范案例）。
- **陷阱盒**：只看 CTR 优化搜索会导致「标题党与信息茧房」——长点击与满意度指标的必要性。
- **实操盒**：用 Python/SQL 搭一个最小可用的倒排索引 + BM25。
- **面试题**：BM25 的参数含义？如何做 query 改写？LTR 三种范式区别？

### ch08 神经检索、重排与 RAG（chapters/ch08-neural-retrieval-rag.tex，`ch:rag`）
- **开篇洞察**：稠密检索把「匹配」变成了「表示学习」，而 RAG 把检索变成了生成的一部分。
- 稠密检索：双编码器（DPR）、训练目标（in-batch negatives、
  hard negatives、ANCE 的异步更新）、
  批内负采样与温度系数的影响、知识蒸馏进双塔。
- 后期交互与多向量：ColBERT 的 MaxSim、
  PLAID 的工程优化、
  稀疏-稠密混合（SPLADE、uniCOIL）、
  混合检索的融合策略（RRF、加权、级联）。
- 向量索引工程：HNSW 原理与参数（M、efConstruction、efSearch）、
  IVF-PQ 与量化、磁盘索引、过滤（pre-filter vs post-filter）、
  召回率-延迟-内存三角。
- 重排：cross-encoder、MonoT5、列表式重排（listwise LLM rerank）、
  级联重排与延迟预算。
- RAG 全景：Naive RAG → Advanced RAG → Modular RAG；
  索引（chunking 策略、父子块、元数据、GraphRAG）、
  检索前（query 改写、HyDE、多查询、路由）、
  检索后（重排、压缩、上下文组装）、
  生成（引用、忠实性、幻觉抑制）。
- RAG 评估：检索侧（Recall@K、MRR、命中率）、
  生成侧（Faithfulness、Answer Relevancy、Context Precision，RAGAS 框架）、
  端到端（人工 + LLM judge）、
  以及「检索对了但答错」与「检索错了但蒙对」的诊断方法。
- Agentic RAG 与工具调用、多跳问答、GraphRAG、记忆机制。
- **案例盒**：企业知识库 RAG 的失败复盘（示范）。
- **陷阱盒**：top-k 越大越好？chunk 越大越好？——上下文噪声与「lost in the middle」。
- **实操盒**：一份 RAG 系统调参清单（chunk 大小、重叠、k、重排模型、温度、引用策略）。
- **面试题**：DPR 的负采样怎么设计？RAG 如何评估？如何解决幻觉？

### ch09 NLP 与预训练语言模型（chapters/ch09-nlp-pretraining.tex，`ch:nlp`）
- **开篇洞察**：NLP 的十年，是从「特征工程」到「表示学习」再到「规模化 + 对齐」的十年。
- 文本表示演进：one-hot → 分布假设 → Word2Vec（CBOW/Skip-gram、负采样、层次 softmax）→
  GloVe → FastText（subword）→ ELMo（上下文相关）。
- Transformer：自注意力公式与复杂度、多头、位置编码（正弦/可学习/RoPE/ALiBi）、
  残差与 LayerNorm（Pre-LN vs Post-LN）、
  为什么比 RNN 好（并行、长程依赖）、计算与显存复杂度分析。
- 预训练范式：自回归（GPT）vs 自编码（BERT）vs 编码-解码（T5）、
  预训练任务（MLM、NSP、Span Corruption、ELECTRA 的替换检测）、
  数据规模与质量（去重、过滤、配比）、
  Scaling Laws 与 Chinchilla 的最优配比、训练成本估算。
- 微调与对齐：全参数微调、PEFT（LoRA/QLoRA/Prefix/P-Tuning）原理与显存收益、
  指令微调（SFT）、RLHF（RM + PPO）、DPO 与 GRPO、
  对齐税（alignment tax）与能力损失。
- 推理与部署：KV Cache、MQA/GQA、FlashAttention、量化（INT8/INT4/GPTQ/AWQ）、
  vLLM 的 PagedAttention、投机解码、连续批处理（continuous batching）、
  推理成本估算公式（tokens × 单价 × 请求量）。
- 评测：传统基准（GLUE/SuperGLUE）、
  生成评测（BLEU/ROUGE/BERTScore）、
  大模型评测（MMLU/GSM8K/HumanEval）、
  以及「评测集污染」「LLM-as-judge 偏差」问题。
- **案例盒**：一个中文垂域模型的训练与部署成本拆解（示范量级）。
- **陷阱盒**：微调 ≠ 知识注入；RAG ≠ 长上下文；「上下文越长越好」的误区。
- **实操盒**：LoRA 微调的关键超参表（rank/alpha/lr/target_modules）与显存估算。
- **面试题**：Transformer 复杂度？BERT 与 GPT 的区别？LoRA 为什么有效？

### ch10 NLP 应用与大模型工程化（chapters/ch10-nlp-applications.tex，`ch:nlpapp`）
- **开篇洞察**：业务里 80% 的收益来自「把任务定义清楚 + 把数据闭环建起来」，而不是换更大的模型。
- 文本分类与情感分析：FastText/BERT/LLM 三种方案的取舍与成本对比、少样本与零样本。
- 序列标注与信息抽取：CRF、BiLSTM-CRF、BERT-NER、
  关系抽取、事件抽取、UIE 统一抽取范式、
  电商场景：属性抽取、评论观点抽取、标题生成。
- 文本匹配与语义相似：Siamese、交互式、句向量质量评估（STS）。
- 生成任务：摘要（抽取式 vs 生成式、事实一致性）、
  翻译（低资源、术语一致性、CAT 工具）、
  文案生成（广告文案、商品描述、SEO 内容）与合规审查。
- 检索增强与知识图谱结合：实体链接、知识图谱补全。
- 多模态：CLIP 的对比学习、图文匹配在电商的应用（
  以图搜图、图像标签、视频理解）、OCR + 版面分析。
- 大模型工程化：Prompt 工程（few-shot、CoT、自洽性、
  结构化输出与 JSON schema 约束）、
  函数调用与 Agent 架构（规划-工具-记忆-反思）、
  评测与回归测试（LLM pipeline 的 CI）、
  成本与延迟优化（缓存、路由小模型、批处理、流式输出）、
  安全与合规（注入攻击、数据泄漏、内容审核、隐私脱敏）。
- 数据闭环：标注平台、主动学习、弱监督、合成数据与自我进化。
- **案例盒**：商品标题生成与 SEO 关键词融合的 pipeline（示范）。
- **陷阱盒**：LLM 生成内容直接上线 SEO 的反效果（质量与政策风险）。
- **实操盒**：LLM 应用的成本-延迟-质量三角调优清单。
- **面试题**：如何用 LLM 做信息抽取并保证稳定性？如何做 Prompt 版本管理？

---

## 第 4 部分 计算广告

### ch11 计算广告：生态与机制设计（chapters/ch11-computational-advertising.tex，`ch:ad`）
- **开篇洞察**：广告系统是「算法 + 经济学」的交叉体，机制设计决定了算法的目标。
- 广告生态图谱：广告主、代理商、DSP、ADX、SSP、媒体、监测方、
  各方的收入模式与利益诉求；RTB 的实时链路（
  曝光请求 → 竞价 → 出价 → 拍卖 → 展示 → 计费 → 归因）与延迟预算（100ms 内）。
- 计费方式：CPM/CPC/CPA/oCPM/oCPC/oCPA/CPT/CPI，
  相互换算（呼应 eCPM 公式），以及广告主视角的 ROI/ROAS 计算。
- 拍卖机制：第一价格与第二价格（Vickrey）、GSP 的定价公式与
  纳什均衡性质、VCG、
  保留价（reserve price）与底价策略、
  第一价格化趋势及其对出价策略的影响（出价着色 bidding shading）。
- 机制设计要点：激励相容、个体理性、收益等价定理、
  质量分（quality score）如何同时调节收入与体验、
  以及「平台收入 vs 广告主 ROI vs 用户体验」的三方平衡。
- 广告类型与产品形态：搜索广告（关键词、匹配模式、
  否定词、质量分构成）、
  信息流广告、展示广告、视频广告（YouTube 的
  可跳过插播、Bumper、信息流视频）、
  电商站内广告（
  关键词竞价、商品推广、品牌广告、DSP 与站内广告的差异）。
- 定向与隐私：人群定向的演进（人口属性 → 行为 → 相似人群 → 模型定向）、
  三方 Cookie 退场与隐私沙盒、
  苹果 ATT 的影响、
  数据合规（GDPR、CCPA、PIPL）对定向能力的实际限制。
- 品牌与效果：品牌广告的度量难题、
  增量实验（geo holdout、PSA、ghost ads）、
  品效协同与全链路归因。
- **案例盒**：Google Ads 质量分如何影响实际 CPC（示范计算）。
- **陷阱盒**：只看 ROAS 会导致「收割品牌流量」——新客与老客必须分开看。
- **实操盒**：一份媒体采购的谈判与考核指标清单。
- **面试题**：GSP 为什么不是激励相容的？oCPC 的原理？如何做增量实验？

### ch12 广告建模、出价与归因（chapters/ch12-ad-modeling-bidding.tex，`ch:admodel`）
- **开篇洞察**：广告算法的核心链条是「预估准 → 出价巧 → 花钱稳 → 归因清」。
- CTR/CVR 预估：特征体系（用户/广告/上下文/交叉）、
  样本与延迟反馈（CVR 的延迟窗口与
  ES-DFM/归因窗口建模）、
  多任务联合建模（CTCVR = CTR × CVR 的
  ESMM 及其后续）、
  校准与出价的关系（
  pCTR 高估会导致超支）。
- 出价策略：从 CPC/CPM 到 oCPA/oCPC 的演进、
  PID 控制与预算平滑（pacing）、
  线性出价 vs 最优出价（
  最优出价 = 价值 × 转化率 / 折扣因子）、
  多约束出价（预算 + ROI 双约束的拉格朗日解法）、
  强化学习出价（RLB）的建模与风险。
- 预算与流量分配：预算平滑（budget pacing）算法、
  流量预测与机会成本、
  合约广告与竞价广告的混合分配、
  广告与自然结果的混排与竞价深度。
- 归因：单触点（last click/first click）、
  多触点规则（线性、时间衰减、位置法 U 型）、
  数据驱动（Shapley 值、马尔可夫链、生存模型）、
  增量式（geo 实验、PSA、转化提升测试）、
  以及 MMM（营销组合模型）与
  MTA 的分工：MMM 看长期与全局，MTA 看实时与精细。
  含 Shapley 值归因的公式与计算复杂度。
- 反作弊与流量质量：点击欺诈的类型、
  识别特征（IP/UA/点击间隔/转化异常）、
  IVT 标准（MRC 可见性、无效流量分类）。
- 创意与商品选择：动态创意优化（DCO）、
  素材自动生成、创意疲劳监测、
  商品选择（选品与广告投放的联动）。
- **案例盒**：oCPC 出价系数从 1.0 到 1.3 的三周调优记录（示范量级）。
- **陷阱盒**：CVR 延迟反馈导致的「模型欠费」与预算超支。
- **实操盒**：归因模型切换的迁移方案与对账表。
- **面试题**：ESMM 为什么能解决样本选择偏差？如何做 ROI 约束出价？

---

## 第 5 部分 流量获取：SEO、GEO 与付费投放

### ch13 SEO：技术、内容与外链（chapters/ch13-seo.tex，`ch:seo`）
- **开篇洞察**：SEO 不是「讨好算法」，而是「把网站做成算法能理解、用户愿意信任的样子」。
- 搜索引擎如何工作：抓取（
  爬虫预算 crawl budget、robots.txt、
  sitemap、抓取频率、日志分析）、
  索引（canonical、noindex、
  重复内容、分面导航、
  JS 渲染与 SSR/ISR）、
  排名（
  相关性、质量、可用性、上下文四个维度）。
- 关键词研究：搜索意图分类（
  导航/信息/商业调研/交易）、
  关键词挖掘方法（
  搜索建议、相关搜索、
  PAA、竞品、GSC、工具）、
  关键词分层（头部/中部/长尾）与
  主题聚类（topic cluster / pillar-cluster 模型）、
  关键词难度与优先级打分公式。
- 站内优化（On-page）：标题标签、H 标签层级、
  URL 结构、内链与锚文本、
  图片 alt 与文件名、
  结构化数据（Schema.org 的
  Product/Article/FAQ/Breadcrumb/Organization 等）、
  页面体验与 Core Web Vitals（LCP/INP/CLS 的定义、阈值与优化手段）。
- 内容策略：E-E-A-T（
  Experience/Expertise/Authoritativeness/Trustworthiness）
  的可操作化、
  内容质量评估框架、
  AI 生成内容的风险与边界、
  内容更新与「内容衰减」治理、
  转化型内容与信息型内容的配比。
- 技术 SEO 清单：站点架构、
  移动端优先、
  hreflang 与多语言多地区（
  跨境电商必做）、
  分页与参数处理、
  404/301 迁移方案、
  XML sitemap 与索引覆盖率诊断、
  日志文件分析寻找抓取浪费。
- 外链与权威：链接价值的判断维度、
  外链获取方式（数字 PR、
  客座、资源页、
  数据研究、HARO）、
  黑帽风险（PBN、链接买卖、
  隐藏链接）与惩罚恢复。
- 度量：GSC 的
  展示/点击/CTR/平均排名、
  第三方工具排名追踪、
  自然流量归因（
  与 GA4 的 not provided 问题）、
  SEO 的实验困境（无法 A/B）与
  替代方法（地理位置分流、
  时间序列因果推断）。
- 跨境电商 SEO 特化：多站点结构（
  子目录 vs 子域名 vs 独立站）、
  多语言内容本地化、
  平台站内 SEO（
  Amazon/Temu/eBay 的 A9/A10 逻辑、
  标题与搜索词字段规则）、
  以及平台 SEO 与独立站 SEO 的差异。
- **案例盒**：一个 DTC 独立站 6 个月自然流量从 0 到 10 万的路径拆解（示范）。
- **陷阱盒**：AI 批量生成内容导致整站被降权；hreflang 配错导致的重复内容。
- **实操盒**：技术 SEO 审计 checklist（60 项，分优先级）。
- **面试题**：Core Web Vitals 三个指标？如何诊断抓取预算浪费？AI 内容能不能做 SEO？

### ch14 GEO / AEO：生成式引擎优化（chapters/ch14-geo-aeo.tex，`ch:geo`）
- **开篇洞察**：搜索正在从「给你十个链接」变成「直接给答案」，
  优化目标从「排名」变成「被引用」。
- 概念辨析：SEO vs AEO（Answer Engine Optimization）
  vs GEO（Generative Engine Optimization）
  vs LLMO；零点击搜索（zero-click）与
  点击率下滑的量化影响。
- 生成式引擎的形态：Google AI Overviews / AI Mode、
  Bing Copilot、Perplexity、
  ChatGPT Search、豆包/元宝/Kimi 等。
- 引用机制（公开研究的综合）：生成式引擎如何选源——
  可提取性（extractability）、
  结构化程度、
  权威信号、
  新鲜度、
  实体一致性、
  多源交叉验证；
  与经典排名的异同（
  排名高不等于被引用，
  但排名是入场券）。
- GEO 技术手段：
  内容分块（
  每段自洽、结论前置、答案块 40–60 字）、
  问答式结构（FAQ、HowTo）、
  数据与引用（一手数据、可验证统计）、
  结构化数据与
  llms.txt / ai.txt 的争议与现状、
  schema 与实体标注、
  页面可抓取性（
  AI 爬虫 UA 管理：GPTBot、Google-Extended、
  ClaudeBot、PerplexityBot 与 robots.txt 策略）。
- 品牌层面的 GEO：品牌实体建设（
  Wikipedia/Wikidata、
  知识面板、
  权威媒体报道）、
  第三方引用源布局（
  行业媒体、评测站、社区、
  Reddit/Quora/知乎）、
  口碑与评论一致性。
- 度量与监测：传统排名工具失效后如何衡量——
  提示词覆盖（prompt set）与
  品牌提及率（share of voice in AI answers）、
  引用来源占比、
  AI 引荐流量（GA4 中的 referrer 识别）、
  与「答案准确率」的监控；
  建立 AI 可见性看板的方法。
- 实操策略：内容形态重构（
  对比表、清单、
  参数表、
  权威定义）、
  多平台分发（
  视频/播客/文档，
  因为生成引擎会跨模态取源）、
  以及「成为被引用的原始来源」而非聚合者。
- 时效性与风险：AI 摘要的流量侵蚀、
  平台政策不确定性、
  内容被滥用与品牌安全。
- **案例盒**：某 B2B 品牌通过「原始数据 + 结构化答案块」提升 AI 引用率（示范）。
- **陷阱盒**：把 llms.txt 当成排名魔法；只为 AI 写内容导致人类读者流失。
- **实操盒**：GEO 30 天行动计划 + AI 可见性监测表设计。
- **面试题**：GEO 与 SEO 的核心差异？如何度量 AI 引用？robots.txt 该怎么配？

### ch15 Google Ads 与 YouTube 投流（chapters/ch15-google-youtube-ads.tex，`ch:google`）
- **开篇洞察**：Google Ads 的本质是「用出价买意图」，而 YouTube 是「用内容买注意力」。
- 账户体系：账号/ MCC、
  广告系列（Campaign）→ 广告组（Ad Group）→
  关键词/广告/素材的三层结构、
  预算与出价的层级关系、
  转化目标（
  转化动作、转化价值、归因模型与窗口）。
- 搜索广告：关键词匹配类型（
  广泛/短语/完全 + 否定关键词）、
  质量分（
  预期点击率、广告相关性、落地页体验）与
  实际 CPC 的关系公式、
  RSA 自适应搜索广告的
  素材组合与 Ad Strength、
  搜索词报告与优化循环（
  搜索词 → 否定词 → 匹配类型收敛）。
- 效果最大化广告（Performance Max）：
  资产组（Asset Group）结构、
  信号（受众信号、素材、
  商品 Feed）、
  它与搜索/购物广告的
  渠道归因冲突（
  品牌词收割问题）、
  以及 PMax 的
  分层控制手段（
  账户级否定词、
  品牌排除、
  出价与预算）。
- 购物广告与 Feed：Merchant Center 的
  Feed 规范（
  GTIN、标题、描述、
  图片、
  价格与库存同步）、
  Feed 优化对点击与转化的影响、
  商品分组的出价策略、
  以及 Feed 报错排查。
- YouTube 广告：广告形态（
  可跳过插播 In-Stream Skippable、
  不可跳过、
  Bumper 6 秒、
  In-Feed 视频、
  Shorts 广告）、
  计费（CPV/CPM/CPE）、
  定向（
  受众、兴趣、
  自定意向、
  再营销、
  类似受众）、
  频道与网红合作（
  YouTube 创作者合作、
  品牌内容）、
  创意方法论（
  前 5 秒钩子、
  品牌回忆 vs 直接转化、
  长短版素材配比）。
- 出价策略：Manual CPC
  → tCPA/tROAS
  → Maximize Conversions
  → Maximize Conversion Value，
  各自适用场景、
  学习期（learning period）与
  数据量门槛（
  30 天 30–50 次转化）、
  以及频繁改动导致的
  「学习期反复重启」。
- 受众与定向：受众细分（
  亲和力、
  有购买意向、
  详细人口统计、
  你的数据）、
  受众排除、
  观察模式 vs 定向模式、
  以及
  Customer Match 与
  隐私合规。
- 度量与优化：转化追踪
  （GA4 导入、gtag、
  增强型转化、
  离线转化导入）、
  归因模型
  （数据驱动归因 DDA、
  Google Ads 内的
  last-click 与数据驱动的差异）、
  与
  Google Ads 数据
  与
  后台真实订单
  对账的方法。
- 预算与节奏：日预算与实际花费的关系、
  支出上限、
  季节性预算调整、
  以及
  「预算受限 vs 出价受限」的诊断。
- **案例盒**：一个 DTC 品牌从 tCPA 到 tROAS 的切换实验（含指标对照表，示范）。
- **陷阱盒**：PMax 把品牌词算作新客；
  tROAS 设太高导致量级崩塌。
- **实操盒**：Google Ads 账户诊断 checklist（
  结构、素材、出价、否词、
  追踪、落地页六大块）。
- **面试题**：质量分如何影响 CPC？PMax 与搜索广告怎么分工？

### ch16 Meta、TikTok 与其他付费渠道（chapters/ch16-meta-tiktok-ads.tex，`ch:meta`）
- **开篇洞察**：在 Meta 和 TikTok 上，素材就是定向，创意即策略。
- Meta 广告体系：账户结构
  （Campaign → Ad Set → Ad）、
  目标（
  认知/流量/互动/潜在客户/应用推广/销售）、
  Advantage+ 系列
  （Advantage+ 购物广告、
  Advantage+ 受众、
  自动素材）、
  版位（
  Facebook/Instagram/Reels/Stories/Audience Network）
  与
  自动版位的影响。
- 定向：核心受众
  （人口、兴趣、行为）、
  自定义受众
  （网站 Pixel、App、
  客户名单、
  互动）、
  类似受众（Lookalike 1%–10%）、
  以及
  广泛定向（Broad）
  在
  算法成熟后的回归——
  讲清「定向收窄 vs 放量」的取舍。
- 信号与追踪：Meta Pixel、
  Conversions API（CAPI）、
  事件去重（event_id）、
  Aggregated Event Measurement（AEM）、
  iOS ATT 后的
  信号损失与
  建模转化（
  1-day click / 7-day click 口径差异）、
  以及
  server-side tagging（
  GTM SS、Stape）
  的部署要点。
- 素材工程（核心章节）：
  素材矩阵（
  钩子类型 ×
  卖点 ×
  形式 ×
  人群）、
  3 秒留存率与
  完播率、
  素材生命周期与
  疲劳识别
  （
  Frequency、
  CTR 下滑、
  CPA 上升）、
  UGC 与
  达人素材、
  批量生产流水线
  （脚本模板、
  拍摄 SOP、
  剪辑模板）、
  以及
  素材测试方法论
  （
  同预算下的
  A/B、
  素材级 vs 广告级测试、
  「素材测试预算」的分配）。
- TikTok 广告：TikTok Ads Manager、
  竞价广告形态
  （信息流、Spark Ads、
  品牌挑战、
  开屏）、
  Spark Ads 与
  自然流量的复用、
  内容原生度要求、
  达人矩阵
  （
  头部引爆 + 腰尾部铺量）、
  直播承接
  （
  GMV = 曝光 ×
  进入率 ×
  停留 ×
  转化率 ×
  客单）、
  以及
  TikTok Shop 的
  内容-交易闭环。
- 其他渠道：Snapchat、
  Pinterest、
  Reddit、
  X、
  联盟网络、
  Google Discovery/Demand Gen、
  以及
  DSP 程序化购买
  （
  The Trade Desk、
  Criteo、
  RTB House）
  的定位与
  适用场景。
- 冷启动与放量方法论：
  测试期（
  多素材小预算）
  → 放量期
  （
  CBO/ABO、
  预算加倍节奏、
  扩量受众）
  → 稳定期
  （
  素材迭代节奏、
  再营销与
  老客复购分离）；
  以及
  「学习期」与
  「50 次转化」门槛的实操含义。
- 归因与对账：平台
  归因窗口差异导致的
  「平台都说是我的功劳」、
  三方差值
  （平台 A + 平台 B > 实际订单）
  的原因与
  增量测试方法
  （
  地理 holdout、
  PSA、
  品牌词暂停测试）。
- **案例盒**：一周 30 条素材的批量生产与测试结果分布（示范）。
- **陷阱盒**：扩量时同时改受众+出价+素材，无法归因；
  依赖平台「转化数」判断真实增量。
- **实操盒**：素材生产 SOP 模板 + 投放日报表字段设计。
- **面试题**：ATT 之后如何做 Meta 投放？如何判断素材疲劳？如何做增量实验？

### ch17 落地页、CRO、邮件与联盟营销（chapters/ch17-cro-email-affiliate.tex，`ch:cro`）
- **开篇洞察**：流量成本只会越来越贵，转化率是唯一能自己控制的杠杆。
- 落地页设计：信息层级与
  5 秒法则、
  首屏要素
  （价值主张、
  视觉证据、
  CTA、
  信任元素）、
  与广告文案的
  一致性（message match）、
  移动端优先的
  排版与
  表单设计
  （字段数与转化率的关系）、
  速度优化
  （
  图片、
  CDN、
  第三方脚本治理）
  与
  Core Web Vitals 的商业影响。
- CRO 方法论：假设生成
  （
  数据 + 用户研究 + 启发式）、
  ICE/PXL 优先级打分、
  测试设计
  （
  样本量计算、
  最小可检测效应 MDE、
  测试时长与
  星期效应）、
  工具
  （GA4、
  Hotjar/Clarity 录屏与热图、
  VWO/Optimizely）、
  以及
  「

  赢家被推翻」的
  复现性问题。
- 转化漏斗诊断：从
  曝光 → 点击 → 落地 →
  加购 → 结账 → 支付
  的逐层流失率
  （基准量级参考）、
  支付失败与
  弃购挽回、
  运费与
  税费展示时机对
  转化的影响。
- 邮件与私域：列表获取
  （
  弹窗、
  内容磁铁、
  结账订阅）、
  生命周期邮件
  （
  欢迎、
  弃购、
  浏览放弃、
  复购、
  唤醒、
  winback）、
  分段与
  个性化、
  送达率
  （
  SPF/DKIM/DMARC、
  域名预热、
  互动度管理）、
  自动化流程
  （Flow）
  与
  广播
  （Campaign）
  的配比、
  以及
  收入占比基准。
- 短信与推送、WhatsApp Business、
  社群运营
  （
  Facebook Group、
  Discord）
  的适用场景。
- 联盟与红人营销：
  联盟网络
  （
  ShareASale、
  CJ、
  Awin、
  Impact）、
  佣金结构设计
  （
  CPS/CPC/CPA、
  阶梯佣金）、
  追踪与
  归因冲突、
  红人分层
  （
  头部/腰部/尾部/KOC）、
  合作模式
  （
  纯佣金、
  坑位费 + 佣金、
  买断、
  白名单投放）、
  以及
  UGC 素材授权
  （whitelisting）
  的投放价值。
- 复购与 LTV：RFM 分层、
  订阅制与
  会员体系、
  交叉销售与
  捆绑、
  以及
  LTV/CAC 的
  计算口径与
  回本周期
  （payback period）。
- **案例盒**：把弃购邮件从 1 封增加到 3 封的收入变化（示范量级）。
- **陷阱盒**：CRO 测试样本不足就下结论；
  邮件群发导致域名信誉崩塌。
- **实操盒**：落地页优化 checklist（30 项）+ 邮件流程蓝图。
- **面试题**：如何计算 A/B 测试所需样本量？如何提升邮件送达率？

---

## 第 6 部分 跨境电商与供应链

### ch18 跨境电商全景与合规（chapters/ch18-cross-border-ecommerce.tex，`ch:cbec`）
- **开篇洞察**：跨境电商 = 电商 + 国际贸易，多出来的是「物流、关税、合规、汇率」四座山。
- 市场格局：主要市场
  （美国、
  欧洲、
  东南亚、
  中东、
  拉美、
  日韩）
  的规模、
  增长、
  消费习惯与
  支付偏好；
  中国出海的
  四波浪潮
  （
  平台铺货 → 精品独立站 →
  品牌 DTC →
  全托管/内容电商）。
- 商业模式分类：
  铺货型、
  精品型、
  品牌型、
  平台型、
  独立站 DTC、
  全托管/半托管；
  各自的
  资金周转、
  库存风险、
  团队配置与
  毛利结构对比表。
- 平台选择：Amazon、
  eBay、
  Walmart、
  Temu、
  TikTok Shop、
  SHEIN、
  Etsy、
  Shopee/Lazada、
  Ozon、
  Coupang、
  Mercado Libre；
  对比维度
  （
  流量、
  佣金、
  门槛、
  履约、
  账期、
  政策风险）。
- 独立站技术栈：Shopify/Shopline/
  WooCommerce/
  自研、
  主题与
  应用生态、
  多币种与
  多语言、
  支付网关
  （
  Stripe、
  PayPal、
  Adyen、
  本地支付
  如
  Klarna、
  iDEAL、
  Pix、
  Boleto）、
  以及
  风控与
  拒付
  （chargeback）
  管理。
- 物流模式：直邮
  （
  邮政小包、
  专线、
  商业快递）、
  海外仓
  （
  自建 vs 第三方、
  FBA、
  平台仓）、
  FBA 与
  FBM 的取舍、
  头程方式
  （
  海运整柜/拼箱、
  空运、
  铁路、
  卡航）
  的
  时效-成本表、
  尾程派送商
  （
  USPS、
  UPS、
  FedEx、
  DHL、
  Royal Mail、
  DPD）
  与
  物流时效对
  转化与
  退款的影响。
- 关税与税务：
  美国
  （
  321 条款 de minimis、
  Section 301 加征、
  sales tax 的
  nexus 与
  marketplace facilitator 规则）、
  欧盟
  （
  IOSS/OSS、
  VAT 税率差异、
  2021 电商增值税改革、
  低值包裹取消免税）、
  英国
  （
  UK VAT、
  CDS）、
  以及
  关税计算方式
  （
  HS 编码、
  完税价格、
  DDP vs DDU/DAP）。
  明确写出
  「关税与 de minimis 规则变动频繁，
  以最新官方公告为准」。
- 合规与责任：
  产品认证
  （
  CE、
  FCC、
  UL、
  CPC、
  REACH、
  RoHS、
  GPSR）、
  知识产权
  （
  商标、
  专利、
  版权、
  外观设计，
  以及
  平台投诉与
  冻结资金的处理）、
  数据合规
  （
  GDPR、
  CCPA、
  PIPL、
  Cookie 同意）、
  广告合规
  （
  FTC 的
  网红披露要求、
  医疗与
  减肥类
  敏感品）、
  以及
  税务合规
  （
  国内出口退税、
  9810/9710/9610 监管代码、
  香港/新加坡
  中转架构的
  合法边界）。
- 收款与资金：
  收款工具
  （
  Payoneer、
  PingPong、
  Airwallex、
  WorldFirst）、
  汇率风险与
  锁汇、
  资金周转周期
  （
  采购账期、
  平台账期、
  库存占用）
  与
  现金流模型。
- 团队与组织：最小可行团队配置
  （
  选品、
  运营、
  投放、
  供应链、
  客服）、
  能力模型与
  薪酬结构、
  以及
  外包
  （
  客服、
  设计、
  拍摄）
  的边界。
- **案例盒**：一个 10 人团队的 SKU 从 0 到 月销 50 万美元 的成本结构拆解（示范量级）。
- **陷阱盒**：忽略 VAT 导致的
  账号冻结与
  追溯补税；
  de minimis 政策变化
  对
  直邮模型的
  冲击。
- **实操盒**：跨境财务模型
  （
  单位经济模型表格模板：
  售价、
  货值、
  头程、
  关税、
  仓配、
  佣金、
  支付、
  退货、
  广告、
  净利）。
- **面试题**：DDP 与 DDU 的区别与风险？如何设计一个跨境的现金流模型？

### ch19 Temu、SHEIN、TikTok Shop 平台模式（chapters/ch19-platforms-temu-shein-tiktok.tex，`ch:platform`）
- **开篇洞察**：这三家不是在「做电商」，而是在把「中国供应链的产能」用算法和物流
  直接接到海外消费者，中间的所有加价环节都被压缩。
- 全托管 vs 半托管 vs 自主运营：
  定义、
  责任划分
  （
  定价权、
  物流、
  售后、
  流量）、
  卖家角色
  （
  供货商 vs 商家）、
  结算方式
  （
  供货价 vs
  结算价、
  账期）、
  以及
  三种模式
  对
  卖家能力的要求
  与
  利润结构
  （对比表）。
- Temu 模式拆解：
  起步于
  全托管
  （卖家只负责供货到平台国内仓，
  平台负责定价、营销、
  物流、
  售后）、
  到
  半托管
  （
  卖家负责海外仓发货）
  与
  本地仓模式
  的演进；
  核价机制
  （
  比价与
  压价逻辑）、
  买手制与
  选品流程、
  JIT 与
  备货模式、
  罚款与
  售后规则、
  「
  低价 + 社交裂变 + 超级碗投放」
  的增长打法、
  以及
  卖家的
  真实利润率
  与
  风险
  （
  被压价、
  库存滞销、
  罚款）。
- SHEIN 模式拆解：
  小单快反
  （
  首单 100 件
  级别的小批量试单 +
  数据反馈后
  快速返单）、
  柔性供应链
  （
  广州番禺的
  产业带集群、
  打样到上架
  最短 3–7 天）、
  数字化选品
  （
  趋势抓取、
  测款）
  与
  库存周转
  （
  个位数天数）
  的
  经济学意义。
  平台化转型
  （SHEIN Marketplace
  与
  第三方卖家招商）
  的规则。
- TikTok Shop 模式拆解：
  内容-交易一体
  （
  短视频/直播 →
  商品卡 →
  小店成交）、
  美区
  与
  东南亚
  的差异、
  全托管
  （
  卖家供货）
  与
  自运营
  （
  达人分销 +
  商家自播）、
  Affiliate 达人分销
  机制
  （
  佣金率、
  样品、
  Open Plan vs
  Targeted Plan）、
  联盟
  （
  机构、
  团长）
  生态、
  直播间的
  人货场
  设计、
  以及
  Fulfilled by TikTok（FBT）
  与
  自发货。
- 平台对比与选择矩阵：
  流量获取难度、
  定价权、
  资金占用、
  毛利、
  门槛、
  合规要求、
  政策风险；
  给出
  「
  什么品适合什么模式」
  的判断路径。
- 平台规则与风控：
  违规类型
  （
  侵权、
  品控、
  虚假宣传、
  刷单、
  价格欺诈）、
  处罚机制
  （
  罚款、
  下架、
  冻结货款、
  封店）、
  以及
  申诉与
  资金解冻
  的实操路径。
- 卖家生存策略：
  多平台分散、
  差异化选品、
  自有品牌、
  私域导流
  （
  合规边界内）、
  以及
  「
  从供货商升级为品牌商」
  的路径。
- **案例盒**：一个工厂型卖家在 Temu 与 TikTok Shop 双平台的不同利润结构（示范量级）。
- **陷阱盒**：全托管的
  「
  看起来没风险」
  ——备货滞销与
  罚款的
  隐性成本。
- **实操盒**：平台入驻与
  首月运营 checklist；
  核价报价的
  成本核算表。
- **面试题**：全托管与半托管的本质区别？SHEIN 的小单快反为什么难复制？

### ch20 选品、供应链与履约（chapters/ch20-supply-chain-selection.tex，`ch:supply`）
- **开篇洞察**：跨境电商的胜负，七分在选品与供应链，三分在流量。
- 选品方法论：
  需求验证
  （
  搜索量、
  趋势工具
  Google Trends、
  平台榜单、
  评论挖掘）、
  竞争分析
  （
  竞品数量、
  评论数分布、
  价格带、
  广告密度）、
  利润测算
  （
  目标毛利率、
  头程与
  关税、
  退货率）、
  以及
  选品打分模型
  （
  多因子加权打分表，
  含权重设计）。
  供应链可行性
  （
  MOQ、
  起订资金、
  交期、
  定制能力）。
- 供应商管理：
  1688/义乌/产业带
  找源方法、
  供应商评估维度
  （
  产能、
  品控、
  交期、
  配合度、
  账期）、
  打样与
  验厂、
  阶梯报价与
  谈判要点、
  多供应商
  备份策略、
  以及
  采购合同与
  质量条款。
- 品控与合规：来料检验
  （IQC）、
  过程检验
  （IPQC）、
  出货检验
  （
  OQC/AQL 抽样标准）、
  客诉与
  质量成本
  （
  预防/鉴定/内部失败/外部失败）、
  以及
  认证准备
  （
  CPC、
  CE、
  FDA 等）。
- 库存与计划：
  需求预测方法
  （
  移动平均、
  指数平滑、
  Holt-Winters、
  机器学习预测）
  与
  预测误差度量
  （MAPE、
  bias）、
  安全库存公式
  （
  $SS = z \cdot \sqrt{LT \cdot \sigma_d^2 + d^2 \cdot \sigma_{LT}^2}$
  ）、
  再订货点
  （ROP）、
  EOQ 模型、
  库存周转率与
  售罄率、
  以及
  滞销处理
  （
  降价、
  清仓、
  捆绑、
  捐赠）。
- 履约与仓配：
  海外仓选址
  （
  靠近消费市场 vs 靠近港口）、
  头程拼柜与
  时效成本权衡、
  尾程派送
  与
  「
  最后一公里」
  成本占比、
  退货逆向物流
  （
  退货率基准、
  退货处理方案
  Returnless Refund）、
  以及
  FBA 的
  仓储费/长期仓储费/移除费
  结构。
- 供应链韧性：
  牛鞭效应
  （Lee 等 1997）
  的成因与
  缓解手段、
  产能约束理论
  （约束理论 TOC）、
  单一来源风险
  与
  产地多元化
  （
  越南、
  印度、
  墨西哥）、
  以及
  地缘政治与
  关税冲击下的
  应对。
- 数字化：
  ERP/OMS/WMS 选型、
  与平台 API 打通、
  数据看板
  （
  库存周转、
  售罄率、
  履约时效、
  缺货率）、
  以及
  自动化补货规则。
- **案例盒**：一款蓝牙耳机从选品到上市的完整成本与周期表（示范量级）。
- **陷阱盒**：只按「毛利率高」选品，忽略体积重与
  关税导致
  实际亏损；
  安全库存算错导致
  旺季后
  大量滞销。
- **实操盒**：选品打分表 + 安全库存计算模板 + 供应商评估表。
- **面试题**：安全库存怎么算？如何应对牛鞭效应？

### ch21 增长闭环：指标、归因与实验（chapters/ch21-growth-loop-analytics.tex，`ch:growth`）
- **开篇洞察**：增长的复利来自「
  数据 → 假设 → 实验 → 沉淀」
  这个循环转得比对手快。
- 指标体系搭建：
  AARRR 与
  RARRA 的对比、
  HEART 框架、
  北极星指标的
  拆解树
  （
  从 GMV 拆到
  UV × CVR × AOV × 复购）、
  指标字典
  （
  口径、
  负责人、
  更新频率）、
  以及
  指标治理
  （
  口径漂移、
  重复计数、
  Goodhart 效应）。
- 数据采集：埋点设计
  （
  事件模型、
  属性设计、
  命名规范）、
  客户端 vs 服务端埋点、
  数据质量监控、
  以及
  GA4 的
  事件-参数模型
  与
  UTM 规范
  （
  utm_source/medium/campaign/content/term 的
  命名规则与
  大小写陷阱）。
- 归因与对账：
  平台归因
  （
  各自的窗口与模型）
  →
  统一口径的
  自建归因
  （
  规则 + 数据驱动）、
  三方差值
  （
  平台后台、
  GA4、
  实际订单）
  的对账表设计、
  MMM 与 MTA 的分工，
  以及
  「
  归因是分配不是真相」
  的认知校准。
- 增量实验：
  A/B 测试的
  假设、
  分流、
  样本量与
  MDE、
  显著性、
  以及
  常见陷阱
  （
  偷看数据、
  多重比较、
  分流污染、
  SRM）；
  无法 A/B 时的
  替代方法
  （
  地理对照、
  时间序列因果推断、
  合成控制、
  断点回归、
  双重差分 DID）。
  CUPED 方差缩减的原理与收益估算。
- 单位经济模型：
  LTV 的计算
  （
  分群、
  留存曲线拟合、
  毛利 LTV vs 收入 LTV）
  与
  CAC 的口径
  （
  混合 CAC vs
  付费 CAC）、
  payback period、
  以及
  不同
  LTV/CAC 目标下的
  投放策略。
- 增长实验的组织：
  实验评审机制、
  实验仓库与
  知识沉淀
  （
  建立
  「实验档案」
  与
  「失败库」）、
  实验文化
  （
  失败的公开与
  复盘）、
  以及
  增长团队
  （
  增长产品、
  数据、
  投放、
  内容）
  的协作模式。
- 自动化与 AI 在增长中的应用：
  自动化投放规则、
  素材批量生成、
  智能出价、
  以及
  预测模型
  （
  LTV 预测、
  流失预警、
  RFM 升级版）。
- **案例盒**：一次「转化率提升 8%」
  实验的
  完整档案
  （
  假设、
  设计、
  样本、
  结果、
  复盘、
  后续）。
- **陷阱盒**：
  用
  「
  最后一次点击」
  做决策导致
  预算错配；
  实验显著但
  业务无感。
- **实操盒**：
  增长实验文档模板
  （
  一页纸）
  +
  指标字典模板
  +
  渠道对账表模板。
- **面试题**：如何设计一次增长实验？如何计算 LTV？平台归因和实际不符怎么办？

---

## 附录

### 附录 A 术语中英对照表（appendix/appA-glossary.tex，`app:glossary`）
按主题分组的 `longtable`：
- 推荐系统（≥ 40 条）
- 搜索引擎与 NLP（≥ 40 条）
- 计算广告（≥ 35 条）
- SEO / GEO / 增长（≥ 40 条）
- 跨境电商与供应链（≥ 40 条）
三列：中文 | English | 一句话解释。用 `\tabhead{}` 表头，`longtable` 支持跨页，表头重复。

### 附录 B 公式速查手册（appendix/appB-formulas.tex，`app:formulas`）
按主题汇总本仓库出现的核心公式（每条附一行说明与出处章节 `\cref{}`）：
相似度与距离、TF-IDF/BM25、矩阵分解与 BPR、FM 二阶项、双塔 softmax、
AUC/GAUC、NDCG/MAP/MRR/Recall@K、LogLoss、
Attention、LayerNorm、Layer 复杂度、
SGD/Adam/LoRA、
eCPM 与质量分 CPC、
GSP/VCG 定价、
最优出价与 PID pacing、
Shapley 归因、
A/B 样本量与 MDE、CUPED、
安全库存与 EOQ、ROP、
LTV/CAC/ROAS/ROI、
漏斗乘法链。用 `formulacard` 盒子或 `align` 环境组织。

### 附录 C 工具、数据源与脚本清单（appendix/appC-toolstack.tex，`app:tools`）
- 算法与工程：Spark/Flink、PyTorch、TensorFlow、Faiss、Milvus、HNSWlib、XGBoost/LightGBM、
  Triton、vLLM、ONNX Runtime、Ray、Kubeflow、MLflow、Feast、Airflow、dbt、
  ClickHouse/Doris/HBase/Redis、Kafka、Elasticsearch/OpenSearch、Lucene、pgvector。
- 分析：GA4、Amplitude、Mixpanel、Metabase、Superset、Jupyter、DuckDB、Polars。
- SEO/GEO：Google Search Console、Bing Webmaster、Ahrefs、Semrush、Screaming Frog、
  Sitebulb、Similarweb、Ahrefs/Semrush、Google Trends、PageSpeed Insights、
  Schema Markup Validator、Rich Results Test。
- 投放：Google Ads / Google Merchant Center / GA4 / Google Tag Manager（含 server-side）、
  Meta Ads Manager / Business Manager / Events Manager、TikTok Ads Manager / Seller Center、
  The Trade Desk、Criteo、Northbeam、Triple Whale、AppsFlyer/Adjust、Segment。
- 跨境：Amazon Seller Central、Temu Seller Center、TikTok Seller Center、SHEIN Seller、
  Shopify/Shopline、Payoneer/PingPong/Airwallex、Stripe/PayPal/Adyen、
  1688/义乌购/Google Trends/Keepa/Jungle Scout、ERP（马帮/店小秘/领星/易仓）。
- `code/` 目录中的示例脚本说明表（脚本名、用途、运行方式）。
- 每条工具写：定位、免费/付费、典型使用场景、一句话坑点。

### 附录 D 面试题库与答题框架（appendix/appD-interview.tex，`app:interview`）
- 分主题题库（每题给 3–8 行答案要点，不是一句空话）：
  - 推荐算法 25 题
  - 搜索与 NLP 20 题
  - 计算广告 20 题
  - SEO/GEO/投放 25 题
  - 跨境与供应链 15 题
  - 数据与实验 15 题
  - 行为面 / 开放题 10 题（含「如何从 0 搭建」「指标跌了怎么排查」「如何做技术选型」）
- 答题框架：STAR、指标拆解法、
  假设-验证法、
  成本-收益法、
  以及
  「
  先问清约束
  」
  的
  开场话术模板。
- 系统设计答题模板：需求澄清 → 规模估算 → 整体架构 → 数据与特征 → 模型选型 → 评估与实验 → 风险与取舍。

### 附录 E 论文与学习资源清单（appendix/appE-papers.tex，`app:papers`）
- 按主题列出必读论文（每条：标题、作者年份、一句话贡献、为什么值得读、难度星级），
  只允许列 `references.bib` 中存在的 key 并 `\cite{}`：
  - 推荐（MF/BPR/FM/DeepFM/DIN/MMoE/PLE/SASRec/BERT4Rec/LightGCN/HSTU/TIGER）
  - 搜索与 IR（VSM/BM25/QL/LTR/DPR/ColBERT/ANCE/SPLADE/FAISS/HNSW）
  - NLP（Word2Vec/GloVe/ELMo/Transformer/BERT/GPT-3/T5/Chinchilla/InstructGPT/LoRA/RAG）
  - 广告（GSP/Vickrey/Myerson/FTRL/FB LR/RTB/oCPC/Shapley 归因）
  - 增长与实验（Trustworthy Online Controlled Experiments、Lean Startup、Hacking Growth）
  - 供应链（bullwhip、Supply Chain Management、Inventory Management、The Goal）
- 学习路径建议：入门 → 进阶 → 前沿，每阶段 8–12 周计划。
- 公开数据集与竞赛：MovieLens、Amazon Reviews、Criteo、Avazu、AliExpress、Taobao、
  MIND、Yelp、MS MARCO、BEIR、MTEB、Kaggle 相关赛题。
- 社区与信息源：arXiv、Papers with Code、SIGIR/KDD/RecSys/WWW/NeurIPS/ACL、
  中文技术博客与公众号类别（不列具体链接，除非确定稳定）。
