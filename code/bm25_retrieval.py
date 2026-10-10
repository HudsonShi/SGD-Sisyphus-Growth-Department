#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
bm25_retrieval.py -- Minimal inverted index + BM25 retrieval (from scratch).

Companion code for <<Growth Tech Notes>> ch07 (Search Engine) and ch01 (BM25 formula).

Usage:
    python3 bm25_retrieval.py

It builds an inverted index over a tiny Chinese doc set (character bigrams as a
cheap stand-in for a real tokenizer), then ranks documents with Okapi BM25 and
prints the top-k results.

BM25:
    score(q, d) = sum_t IDF(t) * f(t,d)*(k1+1) / (f(t,d) + k1*(1-b+b*|d|/avgdl))
    IDF(t)      = log( (N - n_t + 0.5) / (n_t + 0.5) )
"""

from __future__ import annotations

import math
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from typing import Dict, List, Sequence, Tuple

K1 = 1.5   # term-frequency saturation
B = 0.75   # length normalization


def tokenize(text: str) -> List[str]:
    """Character bigrams for CJK + whitespace tokens for ASCII words."""
    text = text.lower()
    tokens: List[str] = []
    for chunk in re.findall(r"[a-z0-9]+|[\u4e00-\u9fff]+", text):
        if re.match(r"^[a-z0-9]+$", chunk):
            tokens.append(chunk)
        else:
            tokens.extend(chunk[i:i + 2] for i in range(max(1, len(chunk) - 1)))
    return tokens


@dataclass
class InvertedIndex:
    docs: Dict[int, List[str]] = field(default_factory=dict)
    postings: Dict[str, Dict[int, int]] = field(default_factory=lambda: defaultdict(dict))
    doc_len: Dict[int, int] = field(default_factory=dict)

    def add(self, doc_id: int, text: str) -> None:
        toks = tokenize(text)
        self.docs[doc_id] = toks
        self.doc_len[doc_id] = len(toks)
        for term, tf in Counter(toks).items():
            self.postings[term][doc_id] = tf

    @property
    def avgdl(self) -> float:
        return sum(self.doc_len.values()) / max(1, len(self.doc_len))

    def idf(self, term: str) -> float:
        n_t = len(self.postings.get(term, {}))
        if n_t == 0:
            return 0.0
        n = len(self.docs)
        return math.log((n - n_t + 0.5) / (n_t + 0.5) + 1e-12)

    def search(self, query: str, top_k: int = 5) -> List[Tuple[int, float]]:
        scores: Dict[int, float] = defaultdict(float)
        avgdl = self.avgdl
        for term in tokenize(query):
            idf = self.idf(term)
            if idf <= 0:
                continue
            for doc_id, tf in self.postings[term].items():
                dl = self.doc_len[doc_id]
                denom = tf + K1 * (1 - B + B * dl / avgdl)
                scores[doc_id] += idf * tf * (K1 + 1) / denom
        return sorted(scores.items(), key=lambda kv: -kv[1])[:top_k]


DOCS: Sequence[str] = [
    "推荐系统召回阶段常用双塔模型，用向量检索做近似最近邻搜索。",
    "搜索引擎的倒排索引把词映射到文档列表，BM25 是经典的相关性打分函数。",
    "计算广告通过实时竞价在第一价格拍卖中完成广告位分配。",
    "跨境电商需要处理头程物流、关税与增值税合规问题。",
    "生成式引擎优化关注内容能否被 AI 摘要引用，而不只是排名。",
    "多目标排序模型用 MMoE 或 PLE 缓解任务之间的跷跷板现象。",
    "BM25 的两个参数 k1 控制词频饱和，b 控制文档长度归一化。",
    "Temu 的全托管模式下卖家只负责供货，平台负责定价与履约。",
]


def main() -> None:
    index = InvertedIndex()
    for i, text in enumerate(DOCS):
        index.add(i, text)

    print(f"indexed docs: {len(DOCS)}, avgdl = {index.avgdl:.2f}\n")
    for query in ["BM25 参数", "双塔 向量检索", "全托管 平台", "关税 增值税"]:
        print(f"query: {query}")
        for doc_id, score in index.search(query, top_k=3):
            print(f"  [{score:6.3f}] doc{doc_id}: {DOCS[doc_id][:38]}...")
        print()


if __name__ == "__main__":
    main()
