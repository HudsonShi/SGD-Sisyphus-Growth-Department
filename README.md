# 增长技术笔记（Growth Tech Notes）

**SGD-Sisyphus-Growth-Department**

> 一本用 LaTeX 写的个人知识库 / 学习路线 / 工程手册。
> 覆盖：**推荐算法 · 搜索引擎 · 计算广告 · NLP · SEO · GEO · 广告投流买量 · 跨境电商与供应链**

---

## 这是什么

一个人可以同时需要的五块知识，被拆成 21 章 + 5 个附录，装订成一本可编译的 PDF 电子书：

| 部分 | 章节 | 核心问题 |
|---|---|---|
| 第 1 部分 基础 | ch01–ch02 | 五个领域共享的底层概念、数学与工程工具 |
| 第 2 部分 推荐算法 | ch03–ch06 | 召回、排序、序列与生成式推荐、系统工程化 |
| 第 3 部分 搜索与 NLP | ch07–ch10 | 倒排索引与 BM25、神经检索与 RAG、预训练与大模型工程 |
| 第 4 部分 计算广告 | ch11–ch12 | 生态与机制设计、CTR/CVR 建模、出价与归因 |
| 第 5 部分 流量获取 | ch13–ch17 | SEO、GEO/AEO、Google/YouTube、Meta/TikTok、CRO 与私域 |
| 第 6 部分 跨境电商 | ch18–ch21 | 全景与合规、Temu/SHEIN/TikTok Shop、选品与供应链、增长闭环 |
| 附录 | A–E | 术语中英对照、公式速查、工具清单、面试题库、论文清单 |

---

## 本书规模

| 章节 | 汉字数 | 章节 | 汉字数 |
|---|---:|---|---:|
| ch01 导论 | 3,990 | ch12 广告建模、出价与归因 | 18,957 |
| ch02 数学、统计与工程基础 | 13,962 | ch13 SEO | 25,476 |
| ch03 推荐系统总论与召回 | 12,171 | ch14 GEO / AEO | 15,488 |
| ch04 排序模型 | 15,235 | ch15 Google Ads 与 YouTube | 20,141 |
| ch05 序列建模与生成式推荐 | 12,156 | ch16 Meta、TikTok 与其他渠道 | 15,562 |
| ch06 推荐系统工程化 | 13,613 | ch17 落地页、CRO、邮件与联盟 | 20,533 |
| ch07 搜索引擎原理与实现 | 12,045 | ch18 跨境电商全景与合规 | 18,729 |
| ch08 神经检索、重排与 RAG | 16,816 | ch19 Temu、SHEIN、TikTok Shop | 19,046 |
| ch09 NLP 与预训练语言模型 | 15,418 | ch20 选品、供应链与履约 | 24,027 |
| ch10 NLP 应用与大模型工程化 | 18,843 | ch21 增长闭环 | 26,669 |
| ch11 计算广告：生态与机制设计 | 17,735 | | |

附录：A 术语中英对照 5,062 / B 公式速查 1,590 / C 工具清单 2,483 /
D 面试题库 37,938 / E 论文与学习资源 17,051。

**合计**：正文与附录约 **42.2 万汉字**，494 个提示框、215 张表、104 幅内联 TikZ 图、443 个带编号公式。
编译产物 **667 页 A4 / 约 4.3 MB**，编译日志里 0 错误、0 缺字、0 未定义引用
（仅 30 处 overfull hbox 的中文断行容差，不影响阅读）。

预编译 PDF 见仓库根目录的 [`growth-tech-notes.pdf`](growth-tech-notes.pdf)（由 CI 每次推送自动重建）。

> 用 `make check` 或 `python3 tools/check.py` 可以随时重新统计（脚本会逐文件输出汉字数、
> 盒子数、表格数、图数与公式数），并顺带做 10 项排版合规检查。

---

## 快速开始

### 依赖

- TeX Live 2023 或更新版本（需要 `xelatex`、`bibtex`、`latexmk`）
- 中文字体：macOS 自带（Songti SC / Heiti SC）即可
- 可选：Python 3（用于 `make wordcount` 统计字数）

> **注意**：本仓库使用 **bibtex + gbt7714** 而非 biblatex/biber，
> 因为部分 macOS 环境下 TeX Live 自带的 `biber` 二进制无法运行。

### 编译

```bash
make            # 完整编译 -> build/main.pdf
make quick      # 只跑一遍 xelatex，快速看排版
make watch      # 监听文件变化自动重编译
make check      # 仓库自检（禁忌字符 / 引用 / 配对 / 字数统计）
make wordcount  # 统计各章汉字数
make clean      # 清理中间文件
make cleanall   # 清理全部（含 PDF）
```

**字体集**：默认 `macnew`（macOS 系统字体）。在 Linux / CI / Overleaf 上用 Fandol：

```bash
make FONTSET=fandol
# 或手动
latexmk -xelatex -usepretex='\def\NotesFontSet{fandol}' main.tex
```

等价的手动命令：

```bash
latexmk -xelatex -interaction=nonstopmode -file-line-error -outdir=build main.tex
```

### Overleaf

上传整个目录，编译器选 **XeLaTeX**，主文档设为 `main.tex`。
若报中文字体缺失，把 `main.tex` 里的 `\providecommand{\NotesFontSet}{macnew}`
改成 `\providecommand{\NotesFontSet}{fandol}`（Overleaf 自带 Fandol 字体）。

### 持续集成

`.github/workflows/build.yml` 在每次 push 时执行三件事：

1. 跑 `tools/check.py --strict`（lint，有 ERROR 即失败）；
2. 用 XeLaTeX + fandol 编译全书，并把 `main.pdf` 作为 artifact 上传；
3. 执行 `code/` 下全部示例脚本，确保它们不会腐坏。

---

## 仓库结构

```
SGD/
 |-- main.tex                  # 主文件：封面、目录、装配全部章节
 |-- notesstyle.sty            # 统一样式：版式、提示框、代码、公式、TikZ 配色
 |-- references.bib            # 参考文献库（GB/T 7714-2015 国标格式）
 |-- STYLE_GUIDE.md            # 写作规范（贡献者必读）
 |-- OUTLINE.md                # 全书详细大纲
 |-- Makefile                  # 构建脚本
 |-- tools/check.py            # 仓库自检脚本（禁忌字符、引用、配对、统计）
 |-- .github/workflows/        # CI：lint + 编译 PDF + 跑示例脚本
 |-- frontmatter/              # 前言、使用说明
 |-- chapters/                 # 正文 21 章
 |-- appendix/                 # 附录 A-E
 |-- code/                     # 可运行的示例脚本
 |-- figures/                  # 图片目录（当前为空，全书插图用内联 TikZ）
 `-- build/                    # 编译产物
```

### 自检

写完或改完内容后跑一遍 lint：

```bash
python3 tools/check.py                       # 全仓库检查 + 字数统计
python3 tools/check.py --strict              # 有 ERROR 时返回非零退出码
python3 tools/check.py chapters/ch13-seo.tex # 只检查一章
```

它会报告：禁忌 Unicode 字符、误加的导言区命令、`\begin/\end` 不配对、
引用了 `references.bib` 中不存在的 key、`\cref` 目标缺失、残留 `\todo`、
代码块内的非 ASCII 字符，以及每章的汉字数 / 提示框 / 表格 / 公式数量。

---

## 排版特性

- **ctexbook** 中文书籍版式，`fontset=macnew`
- 七个自定义提示框：`keypoint`（核心要点）、`insight`（洞察）、`casebox`（案例）、
  `pitfall`（陷阱）、`toolbox`（实操）、`interview`（面试）、`formulacard`（公式）
- `listings` 代码高亮，含自定义 `SQLx` 与 `PyTorch` 语言定义
- `tikz` + `pgfplots` 内联绘图，统一配色（NavyDeep / TealDeep / AmberDeep / CrimsonDeep / VioletDeep）
- `cleveref` 交叉引用（`\cref{ch:seo}` 自动生成「第 13 章」）
- `gbt7714` 国标参考文献格式
- `tabularx` 自适应宽表 + `booktabs` 三线表

写新章节只需：

```latex
\chapter{标题}
\label{ch:new}
\section{小节}
\begin{keypoint}[核心要点]
...
\end{keypoint}
```

然后在 `main.tex` 里加一行 `\input{chapters/chNN-xxx}`。
详细规范见 [`STYLE_GUIDE.md`](STYLE_GUIDE.md)。

---

## 学习路线

**算法工程师路线**
ch02 → ch03 → ch04 → ch05 → ch06 → ch07 → ch08 → ch12

**增长操盘手路线**
ch01 → ch13 → ch14 → ch15 → ch16 → ch17 → ch21

**跨境卖家 / 供应链路线**
ch18 → ch19 → ch20 → ch16 → ch21

---

## 免责声明

广告平台政策、平台招商规则、税务与合规要求（VAT、EPR、DSA、GPSR、de minimis 等）变动极快。
本笔记中的相关描述仅反映写作时的通行做法，**不构成法律、税务或投资建议**。
文中出现的费率、CPM、转化率等数字均为**示范量级**，用于建立直觉，实际请以官方后台与最新文档为准。

---

## License

笔记正文采用 CC BY-NC-SA 4.0；`code/` 目录下的脚本采用 MIT。
