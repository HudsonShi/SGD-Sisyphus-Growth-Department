#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ab_test_planner.py -- Sample size, MDE, duration and CUPED variance reduction.

Companion code for <<Growth Tech Notes>> ch21 (Growth Loop / Experiments).

Key formulas implemented:
    n per arm (two-proportion)  = (z_{1-a/2} + z_{1-b})^2 * (p1(1-p1)+p2(1-p2)) / (p2-p1)^2
    MDE given n                 = solve the same equation for (p2 - p1)
    CUPED variance reduction    = 1 - (1 + theta^2 * var(X) - 2*theta*cov(X,Y)) / var(Y)
                                  with optimal theta = cov(X,Y)/var(X)

Run:
    python3 ab_test_planner.py
"""

from __future__ import annotations

import math
from typing import Tuple


def _z(p: float) -> float:
    """Inverse standard normal CDF via Acklam's rational approximation."""
    a = [-3.969683028665376e+01, 2.209460984245205e+02, -2.759285104469687e+02,
         1.383577518672690e+02, -3.066479806614716e+01, 2.506628277459239e+00]
    b = [-5.447609879822406e+01, 1.615858368580409e+02, -1.556989798598866e+02,
         6.680131188771972e+01, -1.328068155288572e+01]
    c = [-7.784894002430293e-03, -3.223964580411365e-01, -2.400758277161838e+00,
         -2.549732539343734e+00, 4.374664141464968e+00, 2.938163982698783e+00]
    d = [7.784695709041462e-03, 3.224671290700398e-01, 2.445134137142996e+00,
         3.754408661907416e+00]
    plow, phigh = 0.02425, 1 - 0.02425
    if p < plow:
        q = math.sqrt(-2 * math.log(p))
        return (((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) / \
               ((((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1)
    if p > phigh:
        q = math.sqrt(-2 * math.log(1 - p))
        return -(((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) / \
                ((((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1)
    q, r = p - 0.5, (p - 0.5) ** 2
    return (((((a[0] * r + a[1]) * r + a[2]) * r + a[3]) * r + a[4]) * r + a[5]) * q / \
           (((((b[0] * r + b[1]) * r + b[2]) * r + b[3]) * r + b[4]) * r + 1)


def sample_size_per_arm(p1: float, p2: float,
                        alpha: float = 0.05, power: float = 0.80) -> float:
    """Two-proportion sample size per arm (no continuity correction)."""
    z_a, z_b = _z(1 - alpha / 2), _z(power)
    pbar = (p1 + p2) / 2
    return (z_a * math.sqrt(2 * pbar * (1 - pbar)) +
            z_b * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) ** 2 / (p2 - p1) ** 2


def mde(p1: float, n_per_arm: int,
        alpha: float = 0.05, power: float = 0.80) -> float:
    """Smallest detectable absolute lift, solved by bisection."""
    lo, hi = 1e-9, 1 - p1
    for _ in range(200):
        mid = (lo + hi) / 2
        if sample_size_per_arm(p1, p1 + mid, alpha, power) > n_per_arm:
            lo = mid
        else:
            hi = mid
    return hi


def cuped_variance_reduction(var_y: float, var_x: float,
                             cov_xy: float) -> Tuple[float, float]:
    """Return (optimal theta, variance reduction ratio)."""
    theta = cov_xy / var_x
    var_adj = var_y + theta ** 2 * var_x - 2 * theta * cov_xy
    return theta, 1 - var_adj / var_y


def main() -> None:
    base_cvr = 0.030        # 3% conversion rate
    print("=" * 72)
    print(f"baseline CVR = {base_cvr:.2%}, alpha = 0.05, power = 0.80")
    print("=" * 72)
    print(f"{'relative lift':>14}{'abs lift':>10}{'n/arm':>12}{'total users':>14}")
    for rel in [0.05, 0.10, 0.15, 0.20, 0.30]:
        p2 = base_cvr * (1 + rel)
        n = sample_size_per_arm(base_cvr, p2)
        print(f"{rel:>13.0%}{p2 - base_cvr:>10.4f}{n:>12,.0f}{2 * n / 1e4:>11.1f}w")

    print("\n--- MDE for a fixed traffic budget ---")
    for daily in [5_000, 20_000, 100_000]:
        n = daily * 14 / 2                          # 14 days, split 50/50
        print(f"daily UV {daily:>7,} -> n/arm {n:>9,.0f} -> MDE {mde(base_cvr, int(n)):.4%} "
              f"(relative {mde(base_cvr, int(n)) / base_cvr:.1%})")

    print("\n--- CUPED variance reduction ---")
    for rho in [0.0, 0.3, 0.5, 0.7, 0.9]:
        var_y, var_x, cov = 1.0, 1.0, rho * 1.0 * 1.0
        theta, red = cuped_variance_reduction(var_y, var_x, cov)
        print(f"corr(pre-period metric, metric) = {rho:.1f} -> theta = {theta:5.2f}, "
              f"variance reduction = {red:6.1%}, effective sample x{1 / (1 - red):.2f}")


if __name__ == "__main__":
    main()
