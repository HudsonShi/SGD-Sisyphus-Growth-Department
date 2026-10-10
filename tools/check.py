#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tools/check.py -- repository linter for <<Growth Tech Notes>>.

Checks every chapter/appendix .tex file for the rules in STYLE_GUIDE.md:

  1. forbidden Unicode characters (circled digits, box drawing, emoji, arrows,
     math symbols typed literally instead of in math mode)
  2. preamble commands that must never appear in a chapter file
  3. \\begin/\\end environment balance
  4. citation keys that do not exist in references.bib
  5. \\cref/\\ref targets that do not exist anywhere in the repo
  6. leftover \\todo markers
  7. non-ASCII characters inside lstlisting blocks
  8. known footguns: \\mathbb{1}, \\ifnum...>=..., tabularx{\\textwidth} in tcolorbox
  9. \\DeclareMathOperator macros (\\CTR, \\AUC, ...) used outside math mode
  10. statistics: CJK char count, box usage, table/formula/figure counts

Usage:
    python3 tools/check.py              # check all files, print report
    python3 tools/check.py --strict     # exit code 1 if any error is found
    python3 tools/check.py chapters/ch03-recsys-recall.tex
"""

from __future__ import annotations

import argparse
import glob
import os
import re
import sys
from collections import Counter
from typing import Dict, List, Sequence, Set, Tuple

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FORBIDDEN = {
    "circled digits": "①②③④⑤⑥⑦⑧⑨⑩⑪⑫",
    "box drawing": "├└─│┌┐┘┌┼┤┬┴",
    "check/cross/star": "✓✔✗✘★☆※⚠✅❌",
    "unicode arrows": "→←↑↓⇒⇔↔⟶⟵",
    "literal math symbols": "≤≥≠×÷±≈∞∑∏∈∀∃⊂⊆∪∩",
    "fullwidth ASCII": "＝＋－＜＞０１２３４５６７８９"
                       "ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ"
                       "ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ",
    "zero width / NBSP": "\u00a0\u200b\u200c\u200d\ufeff\u3000",
    "emoji-ish": "🔥💡📈📉🚀⭐🎯💬📌",
}
FORBIDDEN_FLAT = "".join(FORBIDDEN.values())

PREAMBLE_CMDS = re.compile(
    r"\\(documentclass|usepackage|begin\{document\}|end\{document\}"
    r"|bibliography|bibliographystyle|printbibliography|addbibresource|part)\b"
)
STUB_MARKER = re.compile(r"\\todo\{")
BEGIN = re.compile(r"\\begin\{([^}]+)\}")
END = re.compile(r"\\end\{([^}]+)\}")
CITE = re.compile(r"\\cite[a-z]*\{([^}]*)\}")
CREF = re.compile(r"\\[cC]ref\{([^}]*)\}")
LABEL = re.compile(r"\\label\{([^}]*)\}")
LSTLISTING_ENV = re.compile(
    r"\\begin\{lstlisting\}(?:\[[^\]]*\])?(.*?)\\end\{lstlisting\}", re.S
)
CODE_MACRO = re.compile(r"\\codefile\{[^}]*\}\{([^}]*)\}")

BOX_ENVS = ["keypoint", "insight", "casebox", "pitfall", "toolbox",
            "interview", "formulacard"]
SECTION = re.compile(r"\\(chapter|section|subsection|subsubsection)\*?\{")
FORMULA_LABELED = re.compile(r"\\label\{(?:eq|formula):")
TABLE_START = re.compile(r"\\begin\{(?:table|longtable|xltabular|sidewaystable)\}")
FIG_START = re.compile(r"\\begin\{(?:figure|tikzpicture)\}")

# 数学环境（\DeclareMathOperator 定义的宏只能在这些环境或 $...$ 内使用）
MATH_ENVS = {
    "equation", "equation*", "align", "align*", "alignat", "alignat*",
    "gather", "gather*", "multline", "multline*", "eqnarray", "eqnarray*",
    "displaymath", "math", "dmath", "dmath*", "flalign", "flalign*",
    "split", "cases", "array", "matrix", "pmatrix", "bmatrix", "vmatrix",
    "Vmatrix", "smallmatrix", "aligned", "gathered", "subequations",
}
# notesstyle.sty 中用 \DeclareMathOperator 定义的算子，只能在数学模式内使用
MATH_ONLY_MACROS = [
    "AUC", "GAUC", "NDCG", "HR", "Recall", "Precision", "MAP", "MRR", "KL",
    "Var", "Cov", "CTR", "CVR", "CPC", "CPM", "ROAS", "ROI", "LTV", "CAC",
    "GMV", "AOV", "ECE", "CPA", "CPT", "CPI", "eCPM", "oCPC", "oCPM", "oCPA",
    "iROAS", "pCTR", "pCVR", "ARPU", "DAU", "MAU", "CTCVR", "CPV", "CPE",
    "CPS", "tCPA", "tROAS", "argmax", "argmin", "softmax", "sigmoid", "relu",
    "concat", "MLP", "Attention", "Fone", "E", "Prob",
]
MACRO_USE = re.compile(r"\\(?:" + "|".join(sorted(MATH_ONLY_MACROS, key=len,
                                                 reverse=True)) + r")(?![A-Za-z])")


def blank_regions(body: str) -> str:
    """Return a copy of body with comments and verbatim regions replaced by
    spaces, so position-based scanning stays aligned with the original."""
    out = list(body)
    # lstlisting / lstlisting-like verbatim environments
    for m in re.finditer(r"\\begin\{(lstlisting|verbatim|Verbatim|minted)\}"
                         r"(?:\[[^\]]*\])?.*?\\end\{\1\}", body, re.S):
        for i in range(m.start(), m.end()):
            if out[i] != "\n":
                out[i] = " "
    # comments (% not preceded by an odd number of backslashes)
    for m in re.finditer(r"(?<!\\)((?:\\\\)*)%.*", body):
        start = m.start() + len(m.group(1))
        end = m.end()
        for i in range(start, end):
            if out[i] != "\n":
                out[i] = " "
    # \\[2pt] line-break-with-space: not a display-math opener
    for m in re.finditer(r"\\\\\[[^\]]*\]", body):
        for i in range(m.start(), m.end()):
            out[i] = " "
    # 单独的 \\ （换行控制符）：必须一起抹掉，否则 `\\AUC` 会被误读成宏 \AUC
    for m in re.finditer(r"\\\\", body):
        for i in range(m.start(), m.end()):
            out[i] = " "
    return "".join(out)


def math_mode_mask(body: str) -> List[bool]:
    """Boolean mask: mask[i] is True when body[i] sits inside math mode."""
    padded = blank_regions(body)
    n = len(padded)
    mask = [False] * n
    env_stack: List[str] = []
    inline = False
    i = 0
    while i < n:
        ch = padded[i]
        if ch == "\\":
            m = re.match(r"\\(begin|end)\{([^}]+)\}", padded[i:])
            if m:
                env = m.group(2)
                if env in MATH_ENVS:
                    if m.group(1) == "begin":
                        env_stack.append(env)
                    elif env_stack and env_stack[-1] == env:
                        env_stack.pop()
                i += m.end()
                continue
            if padded.startswith(r"\[", i) or padded.startswith(r"\]", i):
                if inline or env_stack:
                    mask[i] = mask[i + 1] = True
                inline = not inline
                i += 2
                continue
            if padded.startswith(r"\(", i) or padded.startswith(r"\)", i):
                if inline or env_stack:
                    mask[i] = mask[i + 1] = True
                inline = not inline
                i += 2
                continue
            m = re.match(r"\\[A-Za-z]+|\\.", padded[i:])
            if m:
                # 控制序列本身也要按当前模式标记，否则 \CTR 这类宏
                # 所在位置永远读到 False，产生误报
                if inline or env_stack:
                    for k in range(i, min(i + m.end(), n)):
                        mask[k] = True
                i += m.end()
                continue
        if ch == "$":
            if padded.startswith("$$", i):
                inline = not inline
                i += 2
                continue
            inline = not inline
            i += 1
            continue
        if inline or env_stack:
            mask[i] = True
        i += 1
    return mask


def rel(path: str) -> str:
    return os.path.relpath(path, ROOT)


def strip_comments(text: str) -> str:
    out = []
    for line in text.splitlines():
        idx, esc = -1, False
        for i, ch in enumerate(line):
            if ch == "\\":
                esc = not esc
                continue
            if ch == "%" and not esc:
                idx = i
                break
            esc = False
        out.append(line if idx < 0 else line[:idx])
    return "\n".join(out)


def load_bib_keys() -> Set[str]:
    keys: Set[str] = set()
    path = os.path.join(ROOT, "references.bib")
    if not os.path.exists(path):
        return keys
    with open(path, encoding="utf-8") as fh:
        for m in re.finditer(r"^@[A-Za-z]+\{([^,]+),", fh.read(), re.M):
            keys.add(m.group(1).strip())
    return keys


def load_labels(paths: Sequence[str]) -> Set[str]:
    labels: Set[str] = set()
    for p in paths:
        with open(p, encoding="utf-8") as fh:
            labels |= set(LABEL.findall(fh.read()))
    return labels


def check_file(path: str, bib_keys: Set[str],
               all_labels: Set[str]) -> Tuple[List[str], List[str], Dict[str, int]]:
    errors: List[str] = []
    warns: List[str] = []
    raw = open(path, encoding="utf-8").read()
    body = strip_comments(raw)

    # 1 forbidden characters (report line numbers)
    for lineno, line in enumerate(raw.splitlines(), 1):
        line_nc = line.split("%")[0]
        bad = [c for c in line_nc if c in FORBIDDEN_FLAT]
        if bad:
            kinds = sorted({k for k, v in FORBIDDEN.items()
                            if any(b in v for b in bad)})
            errors.append(f"L{lineno}: forbidden char {bad!r} ({', '.join(kinds)})")

    # 2 preamble commands
    for m in PREAMBLE_CMDS.finditer(body):
        line = body[:m.start()].count("\n") + 1
        errors.append(f"L{line}: forbidden preamble command \\{m.group(1)}")

    # 3 environment balance
    cb, ce = Counter(BEGIN.findall(body)), Counter(END.findall(body))
    for env in sorted(set(cb) | set(ce)):
        if cb[env] != ce[env]:
            errors.append(f"unbalanced environment {env}: "
                          f"{cb[env]} begin vs {ce[env]} end")

    # 4 citation keys
    for m in CITE.finditer(body):
        for key in (k.strip() for k in m.group(1).split(",") if k.strip()):
            if key not in bib_keys:
                line = body[:m.start()].count("\n") + 1
                errors.append(f"L{line}: citation key not in references.bib: {key}")

    # 5 cref targets
    for m in CREF.finditer(body):
        for ref in (r.strip() for r in m.group(1).split(",") if r.strip()):
            if ref not in all_labels:
                line = body[:m.start()].count("\n") + 1
                warns.append(f"L{line}: \\cref target not found in repo: {ref}")

    # 6 leftover todo
    for m in STUB_MARKER.finditer(body):
        line = body[:m.start()].count("\n") + 1
        errors.append(f"L{line}: leftover \\todo placeholder")

    # 7 non-ASCII inside listings
    for m in LSTLISTING_ENV.finditer(body):
        chunk = m.group(1)
        bad = sorted({c for c in chunk if ord(c) > 127})
        if bad:
            line = body[:m.start()].count("\n") + 1
            errors.append(f"L{line}: non-ASCII inside lstlisting: {bad[:8]}")

    # 8 known footguns
    for pat, msg in [(r"\\mathbb\{1\}", "use \\mathbf{1} instead of \\mathbb{1}"),
                     (r"\\ifnum[^\\]*>=", "TeX \\ifnum does not accept '>='"),
                     (r"language=yaml", "language=yaml may be undefined in listings")]:
        for m in re.finditer(pat, body):
            line = body[:m.start()].count("\n") + 1
            warns.append(f"L{line}: {msg}")

    # tabularx{\textwidth} inside tcolorbox
    for box in BOX_ENVS:
        for m in re.finditer(r"\\begin\{" + box + r"\}(.*?)\\end\{" + box + r"\}",
                             body, re.S):
            if re.search(r"tabularx\{\\textwidth\}", m.group(1)):
                line = body[:m.start()].count("\n") + 1
                warns.append(f"L{line}: tabularx{{\\textwidth}} inside {box} box "
                             f"(use \\linewidth)")

    # 9 math-only macros (\DeclareMathOperator) used outside math mode
    mask = math_mode_mask(body)
    for m in MACRO_USE.finditer(body):
        # 跳过 `\\AUC` 这种「换行符 + 普通文本 AUC」的误判：
        # 统计紧邻该反斜杠的连续反斜杠个数，偶数说明它是 \\ 的第二个字符
        j = m.start()
        run = 1
        k = j - 1
        while k >= 0 and body[k] == "\\":
            run += 1
            k -= 1
        if run % 2 == 0:
            continue
        if j < len(mask) and not mask[j]:
            line = body[:m.start()].count("\n") + 1
            snippet = body[max(0, m.start() - 24):m.end() + 18].replace("\n", " ")
            errors.append(f"L{line}: math-only macro \\{m.group(0)[1:]} used outside "
                          f"math mode (missing $...$) | ...{snippet}...")

    stats = {
        "cjk": len(re.findall(r"[\u4e00-\u9fff]", body)),
        "lines": len(raw.splitlines()),
        "boxes": sum(len(re.findall(r"\\begin\{" + b + r"\}", body)) for b in BOX_ENVS),
        "box_kinds": sum(1 for b in BOX_ENVS
                         if re.search(r"\\begin\{" + b + r"\}", body)),
        "tables": len(TABLE_START.findall(body)),
        "figures": len(FIG_START.findall(body)),
        "formulas": len(FORMULA_LABELED.findall(body)),
        "sections": len(SECTION.findall(body)),
        "cites": len({k.strip() for m in CITE.finditer(body)
                      for k in m.group(1).split(",") if k.strip()}),
    }
    return errors, warns, stats


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="*", help="specific .tex files to check")
    ap.add_argument("--strict", action="store_true",
                    help="exit 1 if any error is found")
    args = ap.parse_args()

    if args.files:
        targets = [os.path.abspath(f) for f in args.files]
    else:
        targets = sorted(glob.glob(os.path.join(ROOT, "chapters", "*.tex"))) + \
                  sorted(glob.glob(os.path.join(ROOT, "appendix", "*.tex"))) + \
                  [os.path.join(ROOT, "frontmatter", f)
                   for f in ("preface.tex", "howto.tex")
                   if os.path.exists(os.path.join(ROOT, "frontmatter", f))]

    bib_keys = load_bib_keys()
    # label 来源始终是全仓库，这样单文件检查也能解析跨章 \cref
    repo_tex = sorted(glob.glob(os.path.join(ROOT, "**", "*.tex"), recursive=True))
    all_labels = load_labels(repo_tex)

    total_err = total_warn = 0
    rows: List[Tuple[str, Dict[str, int]]] = []

    print("=" * 88)
    print(f"checking {len(targets)} files, {len(bib_keys)} bib keys, "
          f"{len(all_labels)} labels")
    print("=" * 88)

    for path in targets:
        errors, warns, stats = check_file(path, bib_keys, all_labels)
        rows.append((rel(path), stats))
        total_err += len(errors)
        total_warn += len(warns)
        flag = "FAIL" if errors else ("warn" if warns else " ok ")
        print(f"\n[{flag}] {rel(path)}")
        print(f"        CJK {stats['cjk']:>6}  lines {stats['lines']:>5}  "
              f"sections {stats['sections']:>3}  boxes {stats['boxes']:>3}"
              f"({stats['box_kinds']} kinds)  tables {stats['tables']:>3}  "
              f"figures {stats['figures']:>3}  eq {stats['formulas']:>3}  "
              f"cites {stats['cites']:>3}")
        for e in errors[:12]:
            print(f"        ERROR {e}")
        if len(errors) > 12:
            print(f"        ... and {len(errors) - 12} more errors")
        for w in warns[:6]:
            print(f"        warn  {w}")
        if len(warns) > 6:
            print(f"        ... and {len(warns) - 6} more warnings")

    print("\n" + "=" * 88)
    print(f"{'file':<46}{'CJK':>8}{'lines':>7}{'boxes':>7}{'tab':>5}"
          f"{'fig':>5}{'eq':>5}")
    print("-" * 88)
    for name, s in sorted(rows, key=lambda r: -r[1]["cjk"]):
        print(f"{name:<46}{s['cjk']:>8}{s['lines']:>7}{s['boxes']:>7}"
              f"{s['tables']:>5}{s['figures']:>5}{s['formulas']:>5}")
    print("-" * 88)
    print(f"{'TOTAL':<46}{sum(s['cjk'] for _, s in rows):>8}"
          f"{sum(s['lines'] for _, s in rows):>7}"
          f"{sum(s['boxes'] for _, s in rows):>7}"
          f"{sum(s['tables'] for _, s in rows):>5}"
          f"{sum(s['figures'] for _, s in rows):>5}"
          f"{sum(s['formulas'] for _, s in rows):>5}")
    print("=" * 88)
    print(f"errors: {total_err}   warnings: {total_warn}")

    if args.strict and total_err:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
