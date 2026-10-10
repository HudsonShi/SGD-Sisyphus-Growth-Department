#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
metrics_auc_gauc.py -- AUC, GAUC, NDCG, MRR, Recall@K implemented from scratch.

Companion code for <<Growth Tech Notes>> ch02 (Metrics) and ch01.

Why from scratch: interviewers ask you to derive these, and a wrong
implementation silently ruins offline evaluation.

Run:
    python3 metrics_auc_gauc.py
"""

from __future__ import annotations

import math
import random
from collections import defaultdict
from typing import Dict, List, Sequence, Tuple

random.seed(42)


# --------------------------------------------------------------------------- #
# Classification / ranking metrics
# --------------------------------------------------------------------------- #
def auc(scores: Sequence[float], labels: Sequence[int]) -> float:
    """AUC = P(score of a random positive > score of a random negative).

    Computed with the rank-sum (Mann-Whitney U) formula, O(n log n).
    Ties are handled by average ranks.
    """
    pairs = sorted(zip(scores, labels), key=lambda p: p[0])
    n_pos = sum(labels)
    n_neg = len(labels) - n_pos
    if n_pos == 0 or n_neg == 0:
        return float("nan")

    rank_sum_pos = 0.0
    i = 0
    while i < len(pairs):
        j = i
        while j + 1 < len(pairs) and pairs[j + 1][0] == pairs[i][0]:
            j += 1
        avg_rank = (i + j) / 2.0 + 1.0             # 1-based average rank
        for k in range(i, j + 1):
            if pairs[k][1] == 1:
                rank_sum_pos += avg_rank
        i = j + 1

    return (rank_sum_pos - n_pos * (n_pos + 1) / 2.0) / (n_pos * n_neg)


def gauc(scores: Sequence[float], labels: Sequence[int],
         users: Sequence[int]) -> float:
    """Group AUC: per-user AUC averaged with the user's sample count as weight."""
    by_user: Dict[int, List[Tuple[float, int]]] = defaultdict(list)
    for s, y, u in zip(scores, labels, users):
        by_user[u].append((s, y))

    total_w, acc = 0.0, 0.0
    for u, rows in by_user.items():
        ys = [y for _, y in rows]
        if len(set(ys)) < 2:
            continue                                # user has only one class
        w = len(rows)
        acc += w * auc([s for s, _ in rows], ys)
        total_w += w
    return acc / total_w if total_w else float("nan")


def ndcg_at_k(ranked_labels: Sequence[int], k: int,
              gains: Sequence[float] | None = None) -> float:
    """NDCG@k with binary or graded relevance."""
    g = list(gains) if gains is not None else [float(x) for x in ranked_labels]
    dcg = sum((2 ** g[i] - 1) / math.log2(i + 2) for i in range(min(k, len(g))))
    ideal = sorted(g, reverse=True)
    idcg = sum((2 ** ideal[i] - 1) / math.log2(i + 2) for i in range(min(k, len(ideal))))
    return dcg / idcg if idcg > 0 else 0.0


def recall_at_k(ranked: Sequence[int], relevant: Set[int], k: int) -> float:
    if not relevant:
        return 0.0
    return len(set(ranked[:k]) & relevant) / len(relevant)


def mrr(ranked: Sequence[int], relevant: Set[int]) -> float:
    for i, item in enumerate(ranked, start=1):
        if item in relevant:
            return 1.0 / i
    return 0.0


def logloss(preds: Sequence[float], labels: Sequence[int]) -> float:
    eps = 1e-15
    return -sum(y * math.log(max(p, eps)) + (1 - y) * math.log(max(1 - p, eps))
                for p, y in zip(preds, labels)) / len(labels)


# --------------------------------------------------------------------------- #
# Demo: why AUC can go up while GAUC goes down
# --------------------------------------------------------------------------- #
def demo() -> None:
    print("=" * 68)
    print("AUC / GAUC / NDCG / MRR / Recall@K / LogLoss")
    print("=" * 68)

    scores = [random.gauss(0, 1) for _ in range(400)]
    labels = [1 if s + random.gauss(0, 0.8) > 0.3 else 0 for s in scores]
    users = [i % 20 for i in range(400)]
    print(f"AUC   = {auc(scores, labels):.4f}")
    print(f"GAUC  = {gauc(scores, labels, users):.4f}")

    ranked = [3, 1, 9, 7, 5, 2]
    rel = {3, 9, 2}
    print(f"\nNDCG@3 = {ndcg_at_k([1, 0, 1, 0, 0, 1], 3):.4f}")
    print(f"MRR    = {mrr(ranked, rel):.4f}")
    print(f"Recall@3 = {recall_at_k(ranked, rel, 3):.4f}")

    preds = [0.9, 0.8, 0.2, 0.1]
    print(f"LogLoss  = {logloss(preds, [1, 1, 0, 0]):.4f}")

    print("\n--- Simpson-style trap: global AUC vs per-group AUC ---")
    s2, y2, u2 = [], [], []
    for gid, offset in enumerate([0.0, 3.0]):
        for i in range(60):
            s2.append(random.gauss(offset, 1.0))
            y2.append(1 if i < 30 else 0)
            u2.append(gid)
    print(f"global AUC = {auc(s2, y2):.4f}   GAUC = {gauc(s2, y2, u2):.4f}")
    print("A model that only learns the group offset can win on AUC but lose on GAUC.")


if __name__ == "__main__":
    demo()
