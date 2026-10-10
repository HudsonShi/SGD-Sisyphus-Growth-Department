###############################################################################
#  《增长技术笔记》构建脚本
#  依赖：TeX Live 2023+（xelatex + biber + latexmk）
###############################################################################

MAIN      := main
LATEXMK   := latexmk
LATEXMKFLAGS := -xelatex -interaction=nonstopmode -file-line-error -halt-on-error
OUTDIR    := build

.PHONY: all quick watch clean cleanall bib wordcount check

## 完整编译（含参考文献）
all:
	$(LATEXMK) $(LATEXMKFLAGS) -outdir=$(OUTDIR) $(MAIN).tex
	@echo "==> 输出：$(OUTDIR)/$(MAIN).pdf"

## 仓库自检：禁忌字符 / 引用 key / 环境配对 / 字数统计
check:
	@python3 tools/check.py

## 快速编译：只跑一遍 xelatex，用于看排版
quick:
	xelatex -interaction=nonstopmode -file-line-error -outdir=$(OUTDIR) $(MAIN).tex

## 监听改动自动重编译
watch:
	$(LATEXMK) $(LATEXMKFLAGS) -pvc -outdir=$(OUTDIR) $(MAIN).tex

## 只更新参考文献
bib:
	biber --input-directory=$(OUTDIR) --output-directory=$(OUTDIR) $(MAIN)

## 清理中间文件
clean:
	$(LATEXMK) -c -outdir=$(OUTDIR) $(MAIN).tex
	@rm -f $(MAIN).{aux,bbl,bcf,blg,fls,fdb_latexmk,log,out,run.xml,toc,lof,lot}

## 全部清理（含 PDF）
cleanall:
	$(LATEXMK) -C -outdir=$(OUTDIR) $(MAIN).tex
	@rm -rf $(OUTDIR)/*

## 统计各章字数（按中文字符粗略估计）
wordcount:
	@python3 - <<'PY'
import glob, re, os
rows = []
for f in sorted(glob.glob('chapters/*.tex')) + sorted(glob.glob('appendix/*.tex')):
    t = open(f, encoding='utf-8').read()
    cn = len(re.findall(r'[\u4e00-\u9fff]', t))
    en = len(re.findall(r'[A-Za-z]+', t))
    rows.append((os.path.basename(f), cn, en, len(t.splitlines())))
rows.sort(key=lambda r: -r[1])
print(f"{'file':<42}{'CJK':>8}{'EN-word':>10}{'lines':>8}")
for r in rows:
    print(f"{r[0]:<42}{r[1]:>8}{r[2]:>10}{r[3]:>8}")
print(f"{'TOTAL':<42}{sum(r[1] for r in rows):>8}{sum(r[2] for r in rows):>10}{sum(r[3] for r in rows):>8}")
PY
