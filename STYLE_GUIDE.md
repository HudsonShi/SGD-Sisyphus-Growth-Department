# 写作规范（STYLE_GUIDE）—— 必须严格遵守

本仓库是 LaTeX 笔记书《增长技术笔记》。你写的每一个 `.tex` 文件都会被 `main.tex` 用 `\input{}` 引入。
**违反下列任何一条都会导致整本书编译失败。**

---

## 1. 文件结构契约

### 1.1 允许
```latex
\chapter{中文标题}
\label{ch:xxx}

\section{一级小节}
\subsection{二级小节}
\subsubsection{三级小节}
...正文...
```

### 1.2 严禁出现（出现即编译失败）
- `\documentclass` / `\usepackage` / `\begin{document}` / `\end{document}`
- `\bibliographystyle` / `\bibliography` / `\printbibliography`
- `\part{}`（分部由 main.tex 统一控制）
- 重新定义已有宏（`\renewcommand`）
- `\include{}`（只能用 `\input{}`，本仓库实际不需要）

### 1.3 章节文件命名与 label（必须与下表完全一致，不要改）
| 文件 | label |
|---|---|
| chapters/ch02-math-foundations.tex | `ch:math` |
| chapters/ch03-recsys-recall.tex | `ch:recall` |
| chapters/ch04-recsys-ranking.tex | `ch:ranking` |
| chapters/ch05-recsys-sequence-generative.tex | `ch:sequence` |
| chapters/ch06-recsys-engineering.tex | `ch:receng` |
| chapters/ch07-search-engine.tex | `ch:search` |
| chapters/ch08-neural-retrieval-rag.tex | `ch:rag` |
| chapters/ch09-nlp-pretraining.tex | `ch:nlp` |
| chapters/ch10-nlp-applications.tex | `ch:nlpapp` |
| chapters/ch11-computational-advertising.tex | `ch:ad` |
| chapters/ch12-ad-modeling-bidding.tex | `ch:admodel` |
| chapters/ch13-seo.tex | `ch:seo` |
| chapters/ch14-geo-aeo.tex | `ch:geo` |
| chapters/ch15-google-youtube-ads.tex | `ch:google` |
| chapters/ch16-meta-tiktok-ads.tex | `ch:meta` |
| chapters/ch17-cro-email-affiliate.tex | `ch:cro` |
| chapters/ch18-cross-border-ecommerce.tex | `ch:cbec` |
| chapters/ch19-platforms-temu-shein-tiktok.tex | `ch:platform` |
| chapters/ch20-supply-chain-selection.tex | `ch:supply` |
| chapters/ch21-growth-loop-analytics.tex | `ch:growth` |
| appendix/appA-glossary.tex | `app:glossary` |
| appendix/appB-formulas.tex | `app:formulas` |
| appendix/appC-toolstack.tex | `app:tools` |
| appendix/appD-interview.tex | `app:interview` |
| appendix/appE-papers.tex | `app:papers` |

跨章引用请使用 `\cref{ch:recall}`、`\cref{ch:seo}` 这样的形式（`cleveref` 已加载）。

---

## 2. 可用宏与盒子环境（全部已在 notesstyle.sty 中定义，直接用）

### 2.1 行内宏
| 宏 | 效果 | 用途 |
|---|---|---|
| `\term{中文}{English}` | **中文**（*English*） | 术语首次出现 |
| `\code{...}` | 等宽小字 | 内联代码、字段名、后台路径 |
| `\kw{...}` | 加粗蓝色 | 关键概念强调 |
| `\en{...}` | 斜体 | 英文短语 |
| `\metric{...}` | 无衬线 | 指标名，如 `\metric{GAUC}` |
| `\todo{...}` | 红色 TODO | 仅占位用，正式内容不要留 |

### 2.2 盒子环境（**每个章节至少使用 6 次，分布在不同小节**）
```latex
\begin{keypoint}[核心要点]      ... \end{keypoint}     % 结论性总结，蓝
\begin{insight}[洞察]          ... \end{insight}      % 深层理解、反直觉结论，绿
\begin{casebox}[案例：标题]     ... \end{casebox}      % 真实/公开案例，绿框
\begin{pitfall}[常见陷阱]       ... \end{pitfall}      % 易错点，红
\begin{toolbox}[工具与实操]     ... \end{toolbox}      % 可执行步骤/清单/参数，橙
\begin{interview}[面试追问]     ... \end{interview}    % 面试题，紫
\begin{formulacard}[公式速记]   ... \end{formulacard}  % 关键公式，灰
```

### 2.3 定理类环境
`definition` / `example` / `remark` / `theorem` / `lemma` / `proposition` / `corollary`
用法：`\begin{definition}[名称] ... \end{definition}`（可选参数可省略）

### 2.4 数学
`amsmath, amssymb, mathtools, bm` 已加载。可用自定义算子：
`\argmax \argmin \softmax \sigmoid \concat \E \Prob \R \Var \norm{} \abs{} \inner{}{} \T`（转置）

多行公式用 `align`，单行关键公式用 `equation` 并加 `\label{eq:xxx}`。

---

## 3. 编码与字符禁令（**极其重要**）

XeLaTeX 使用的是 Latin Modern Mono / macOS 中文字体，很多 Unicode 符号**没有字形**，会出现黑色方块或 `Missing character` 警告。

### 3.1 严禁出现的字符
- 圈码：`①②③④⑤⑥⑦⑧⑨⑩` ❌ → 改用 `(1) (2) (3)`
- 方框绘制：`├ └ ─ │ ┌ ┐ ┘` ❌ → 目录树改用 `|--` 和 `` `-- ``
- 勾叉星：`✓ ✗ ★ ☆ ※ ⚠ ✅ ❌` ❌ → 改用文字「是 / 否 / 注意」
- 箭头：`→ ← ↑ ↓ ⇒ ⇔` ❌ → 数学模式 `$\to$ $\leftarrow$ $\Rightarrow$ $\Leftrightarrow$`
- 数学符号直接打：`≤ ≥ ≠ × ÷ ± ≈ ∞ ∑ ∏ ∈ ∀ ∃` ❌ → 用 `$\le$ $\ge$ $\ne$ $\times$ $\div$ $\pm$ $\approx$ $\infty$ $\sum$ $\prod$ $\in$ $\forall$ $\exists$`
- Emoji（任何表情符号）❌
- 全角空格、不间断空格（不要从网页直接粘贴）❌

### 3.2 代码块
代码块内**只能用 ASCII**（英文注释、英文变量名）。中文解释写在代码块前后的正文里。

```latex
\begin{lstlisting}[style=growth, language=Python, caption={标题}]
# English comment only
def bpr_loss(u, i, j):
    return -torch.log(torch.sigmoid((u * i).sum() - (u * j).sum()))
\end{lstlisting}
```
可用 `language=`：`Python`、`SQLx`（自定义 SQL）、`bash`、`C++`、`Java`、`Scala`、`json`、`yaml`。
不需要行号的短片段用 `style=growthnoline`。

---

## 4. 表格与插图

### 4.1 表格（优先用 tabularx 铺满版心，避免溢出）
```latex
\begin{table}[htbp]
\centering
\caption{标题}
\label{tab:xxx}
\small
\begin{tabularx}{\textwidth}{L{2.4cm} L{3.2cm} Y}
\toprule
\tabhead{列1} & \tabhead{列2} & \tabhead{列3} \\
\midrule
内容 & 内容 & 内容 \\
\bottomrule
\end{tabularx}
\end{table}
```
列类型：`L{宽}` 左对齐定宽、`C{宽}` 居中定宽、`R{宽}` 右对齐定宽、`Y` 自适应剩余宽度。
长表格用 `longtable`，跨页宽表用 `sidewaystable`（`rotating` 已加载）。

### 4.2 插图：**只用内联 TikZ，不引入外部图片文件**
```latex
\begin{figure}[htbp]
\centering
\begin{tikzpicture}[
  node distance=6mm,
  box/.style={draw=NavyMid, fill=BoxBG, rounded corners=2pt, minimum height=8mm,
              inner sep=4pt, text width=2.6cm, align=center, font=\sffamily\scriptsize}
]
\node[box] (a) {召回};
\node[box, right=of a] (b) {粗排};
\draw[-{Stealth}, thick, SlateGray] (a) -- (b);
\end{tikzpicture}
\caption{标题}
\label{fig:xxx}
\end{figure}
```
可用颜色：`NavyDeep NavyMid TealDeep AmberDeep CrimsonDeep VioletDeep SlateGray BoxBG BoxBGAlt CodeBG RuleGray`。

**TikZ 陷阱**：`.style={draw=#1}` 中若定义了 `#2` 却没有传入两个参数，会报 `Illegal parameter number`。样式需要几个参数就传几个，或把颜色写死在样式里。

pgfplots 可用（`compat=1.18`），坐标轴标签用英文避免字体问题。

---

## 5. 参考文献

只允许引用 `references.bib` 中**已经存在**的 key。
先看可用 key：

```bash
grep -oE '^@[a-zA-Z]+\{[^,]+' references.bib | sed 's/.*{//' | sort
```

引用写法：`\cite{devlin2019bert}`、多篇 `\cite{covington2016youtube,cheng2016widendeep}`。
**不要编造 key。** 如果需要引用某篇论文但 bib 里没有，就用正文文字描述（如「Google 2024 年发布的核心网页指标文档指出……」），不要 `\cite`。

---

## 6. 内容质量要求（这是最重要的部分）

### 6.1 每章必须包含的结构
1. **开篇洞察盒**：`\begin{insight}[本章要解决的问题]`，列出 3–6 个具体问题。
2. **问题定义与业务背景**：这个技术在真实业务中解决什么问题，输入输出是什么。
3. **指标体系**：该领域的关键指标、公式、口径、常见误读。
4. **技术演进脉络**：按时间/复杂度递进讲清「为什么上一代不够用」。
5. **方法论细节**：核心公式 + 直觉解释 + 复杂度/代价分析（不要只堆公式）。
6. **工程实现**：真实系统怎么落地，延迟/内存/样本/一致性等工程约束。
7. **案例盒**：至少 1 个，来自公开论文/公开报道/行业通识（注明来源性质，不要伪造内部数据）。
8. **陷阱盒**：至少 1 个，写清现象、根因、排查方法。
9. **实操盒**：至少 1 个，给出可执行清单、参数表或代码。
10. **本章小结**：`\begin{keypoint}[本章要点回顾]` + 编号列表。
11. **面试题**：`\begin{interview}[本章对应的面试题]` + 4–8 个问题（答案统一放附录 D，正文只列问题）。
12. **过渡句**：结尾 1–2 句自然引出下一章。

### 6.2 篇幅要求
- 每章正文**不少于 6000 个汉字**（重点章节如 ch03/ch04/ch07/ch11/ch13/ch15/ch16/ch18 建议 8000–12000 汉字）。
- 表格 ≥ 3 个，公式 ≥ 5 个（有公式的章节），图（TikZ）≥ 1 个。
- **宁深不浅**：不要写「XX 很重要」这类空话；每段都要有具体信息（数字、参数、公式、对比、失败案例）。

### 6.3 写作风格
- 中文主叙述，专业术语中英对照。
- 多讲**取舍（trade-off）**：为什么选 A 不选 B，代价是什么。
- 数字要标注量级来源性质（「经验值」「公开论文报告」「示范量级」），**禁止编造精确的虚假统计**。
- 平台政策/费率/规则类内容必须写「以官方最新文档为准」。
- 涉及中国出海业务时，注意合规表述（税务、数据、广告政策）。

---

## 7. 自检清单（提交前逐条过一遍）

本仓库自带 lint 脚本 `tools/check.py`，它会检查：禁忌字符、导言区命令、
`\begin/\end` 配对、引用 key 是否存在于 `references.bib`、`\cref` 目标是否存在、
残留 `\todo`、代码块内的非 ASCII 字符，以及已知坑（`\mathbb{1}`、`\ifnum...>=...`、
tcolorbox 内 `tabularx{\textwidth}`），并统计汉字数与盒子/表格/公式数量。

```bash
python3 tools/check.py                       # 检查全部章节
python3 tools/check.py chapters/ch07-search-engine.tex   # 只检查一章
python3 tools/check.py --strict              # 有 ERROR 时返回非零退出码
```

**必须做到：`tools/check.py` 对你负责的文件零 ERROR，且文件可以被 `xelatex` 无错误编译。**

### 7.1 已知本地环境坑（务必避开）

| 坑 | 现象 | 正确写法 |
|---|---|---|
| `\mathbb{1}` | macnew 字体无字形，`Missing character` | `\mathbf{1}` |
| 数学算子用在正文里 | `\CTR \CVR \CPC \CPM \ROAS \ROI \LTV \CAC \GMV \AOV \CPA \eCPM \pCTR \AUC \GAUC \NDCG` 等是 `\DeclareMathOperator` 定义的，**只能在数学模式内用**，否则 `Missing $ inserted` 直接中断编译 | 写 `$\CTR$`，不要写 `\CTR{}`；TikZ 节点文本与表格单元格同理。**正文/表头里想用非斜体缩写时，用 `\metric{CTR}`（无衬线，文本模式可用）** |
| tcolorbox 内放浮动体 | `! LaTeX Error: Float(s) lost.` | 盒内不要用 `\begin{table}`；改用 `\begin{center} ... \captionof{table}{...} \label{...} \end{center}` |
| tcolorbox 内 `tabularx{\textwidth}` | 盒子内容溢出 | 用 `\linewidth` |
| TikZ 样式名 `in` / `out` / `cap` | `Package pgfkeys Error: The key '/tikz/in' requires a value`，Emergency stop | 改名 `inflow` / `obox` / `capnode` 等。**凡是与 pgfkeys 内置键同名的短样式名都有风险**，建议统一加后缀 |
| TikZ 图超出版心 | `Overfull \hbox` | 用 `\resizebox{\textwidth}{!}{...}` 包裹，或重排坐标 |
| `\ifnum\i>=\j` | TeX 的 `\ifnum` 关系符只能是单 token，报 `Missing number` | 写成 `\ifnum\j>\i ... \else ... \fi` |
| `language=yaml`（旧版 listings） | `Package Listings Error: language yaml undefined` | 本仓库已在 `notesstyle.sty` 中自定义 `yaml` 与 `json`；若仍报错就改用 `bash`/`Python` |
| 全角等号/不等号 `＝` `≠` | XeLaTeX 无字形 | 用文字「等于 / 不等于」，或在数学模式里用 `$=$` `$\ne$` |
| macOS 自带 `grep -P` | `invalid option -- P` | 用 `python3 tools/check.py` |

### 7.2 手工检查（可选）

```bash
# 检查 \begin/\end 配对
python3 -c "
import re, sys
from collections import Counter
s = open(sys.argv[1], encoding='utf-8').read()
b = Counter(re.findall(r'\\\\begin\{([^}]+)\}', s))
e = Counter(re.findall(r'\\\\end\{([^}]+)\}', s))
print('unbalanced:', {k: (b[k], e[k]) for k in set(b) | set(e) if b[k] != e[k]})
" chapters/你的文件.tex
```
