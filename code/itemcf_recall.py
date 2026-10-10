#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
itemcf_recall.py -- Item-based collaborative filtering recall, from scratch.

Companion code for <<Growth Tech Notes>> ch03 (Recommendation Recall).

Pipeline:
    1. build user -> items interaction table (synthetic data, no deps)
    2. invert to item -> users
    3. compute item-item cosine similarity with popularity penalty (Swing-like damping)
    4. truncate to top-N neighbours per item  -> i2i index
    5. serve recall for a user by aggregating neighbours of her recent items

Run:
    python3 itemcf_recall.py
"""

from __future__ import annotations

import math
import random
from collections import defaultdict
from typing import Dict, List, Sequence, Set, Tuple

random.seed(7)

N_USERS = 200
N_ITEMS = 120
MIN_CO = 1            # minimum co-occurrence to keep a pair
TOP_N_NEIGHBOURS = 20  # i2i truncation
TOP_K_RECALL = 10


def gen_interactions() -> Dict[int, Set[int]]:
    """Synthetic interactions with latent item clusters (so i2i has signal)."""
    clusters = [list(range(i, i + 15)) for i in range(0, N_ITEMS, 15)]
    user2items: Dict[int, Set[int]] = {}
    for u in range(N_USERS):
        items: Set[int] = set()
        for _ in range(random.randint(1, 3)):
            cluster = random.choice(clusters)
            items |= set(random.sample(cluster, random.randint(3, 8)))
        user2items[u] = items
    return user2items


def build_i2i(user2items: Dict[int, Set[int]]) -> Dict[int, List[Tuple[int, float]]]:
    item2users: Dict[int, Set[int]] = defaultdict(set)
    for u, items in user2items.items():
        for i in items:
            item2users[i].add(u)

    pop = {i: len(us) for i, us in item2users.items()}
    co: Dict[int, Dict[int, int]] = defaultdict(lambda: defaultdict(int))
    for u, items in user2items.items():
        items = sorted(items)
        for a_idx in range(len(items)):
            for b_idx in range(a_idx + 1, len(items)):
                a, b = items[a_idx], items[b_idx]
                co[a][b] += 1
                co[b][a] += 1

    i2i: Dict[int, List[Tuple[int, float]]] = {}
    for a, neighbours in co.items():
        scored: List[Tuple[int, float]] = []
        for b, c in neighbours.items():
            if c < MIN_CO:
                continue
            # cosine-like similarity with popularity damping (alpha = 0.5)
            sim = c / math.sqrt(pop[a] * pop[b]) / (pop[b] ** 0.5)
            scored.append((b, sim))
        scored.sort(key=lambda kv: -kv[1])
        i2i[a] = scored[:TOP_N_NEIGHBOURS]
    return i2i


def recall(user_items: Sequence[int],
           i2i: Dict[int, List[Tuple[int, float]]],
           top_k: int = TOP_K_RECALL,
           max_hist: int = 20) -> List[Tuple[int, float]]:
    scores: Dict[int, float] = defaultdict(float)
    history = list(user_items)[-max_hist:]
    for rank_pos, item in enumerate(reversed(history)):   # newer items weigh more
        decay = 1.0 / math.log2(rank_pos + 2)
        for cand, sim in i2i.get(item, []):
            scores[cand] += sim * decay
    for item in history:
        scores.pop(item, None)                            # do not recommend seen items
    return sorted(scores.items(), key=lambda kv: -kv[1])[:top_k]


def main() -> None:
    user2items = gen_interactions()
    i2i = build_i2i(user2items)
    print(f"users={len(user2items)}  items_with_neighbours={len(i2i)}\n")

    for u in [0, 1, 2]:
        hist = sorted(user2items[u])
        top = recall(hist, i2i)
        print(f"user {u} history ({len(hist)} items): {hist[:8]} ...")
        print("  recall:", [f"item{c}({s:.3f})" for c, s in top])
        print()


if __name__ == "__main__":
    main()
