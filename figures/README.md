# figures/

本目录目前是**空**的，这是有意为之。

全书所有插图（架构图、流程图、对比示意图、模型结构图）都使用 **内联 TikZ / pgfplots**
在章节文件里直接绘制，而不是引入外部 PNG/SVG。这样做的好处：

- 单一来源：图与正文同版本管理，`git diff` 能看见图的变化；
- 矢量输出：任意缩放不糊，打印与屏幕阅读都清晰；
- 配色统一：全部取自 `notesstyle.sty` 中定义的
  `NavyDeep / NavyMid / TealDeep / AmberDeep / CrimsonDeep / VioletDeep / SlateGray / BoxBG / RuleGray`；
- 无需外部素材依赖：克隆下来就能编译出完整 PDF。

什么时候该往这里放文件？只有当某张图**无法用 TikZ 合理表达**时，例如：

- 产品后台的真实截图（带敏感数据，注意脱敏）；
- 需要照片级真实感的 UI 原型；
- 从公开论文中引用且许可证允许转载的图表（请在图注中标注来源与许可）。

放置约定：

```
figures/
  ch13-serp-layout.png      # 命名：章节号-语义描述
  ch16-creative-matrix.png
```

在章节中引用：

```latex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.9\linewidth]{figures/ch13-serp-layout.png}
  \caption{搜索结果页版块布局（截图，已脱敏）}
  \label{fig:serp-layout}
\end{figure}
```

注意：使用外部图片需要保证 `main.tex` 编译时的工作目录是仓库根目录，
否则相对路径会失效（`make` 已经处理好了这一点）。
