#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
crossborder_unit_economics.py -- Unit economics + safety stock + EOQ calculator.

Companion code for <<Growth Tech Notes>> ch18 (Cross-border E-commerce) and
ch20 (Supply Chain & Selection).

Covers:
    1. landed cost build-up (goods + first-mile + duty + last-mile + commission + ads)
    2. break-even price and target-price reverse solve
    3. contribution margin / ROI / payback estimation
    4. safety stock and reorder point
    5. EOQ (economic order quantity)

ALL NUMBERS BELOW ARE ILLUSTRATIVE. Platform fees, duty rates and de minimis
thresholds change frequently -- always verify against the latest official docs.

Run:
    python3 crossborder_unit_economics.py
"""

from __future__ import annotations

import math
from dataclasses import dataclass


# --------------------------------------------------------------------------- #
# 1. Unit economics
# --------------------------------------------------------------------------- #
@dataclass
class Sku:
    name: str
    selling_price: float      # retail price on the storefront (USD)
    cogs: float               # purchase cost from supplier
    first_mile: float         # freight from factory to overseas warehouse
    duty_rate: float          # ad valorem duty + VAT, applied to (cogs + first_mile)
    warehouse_fee: float      # storage + pick & pack per order
    last_mile: float          # last-mile delivery per order
    commission_rate: float    # marketplace / payment commission
    ad_cost_per_order: float  # blended CAC (or CPA) per order
    return_rate: float        # fraction of orders returned
    return_cost: float        # reverse logistics + restock loss per returned order

    def landed_cost(self) -> float:
        return self.cogs + self.first_mile

    def duty(self) -> float:
        return self.landed_cost() * self.duty_rate

    def total_cost(self) -> float:
        base = (self.landed_cost() + self.duty() + self.warehouse_fee +
                self.last_mile + self.ad_cost_per_order +
                self.selling_price * self.commission_rate)
        return base + self.return_rate * self.return_cost

    def net_profit(self) -> float:
        return self.selling_price - self.total_cost()

    def gross_margin(self) -> float:
        return (self.selling_price - self.landed_cost() - self.duty()) / self.selling_price

    def net_margin(self) -> float:
        return self.net_profit() / self.selling_price

    def breakeven_price(self) -> float:
        """Price at which net profit is exactly zero."""
        fixed = (self.landed_cost() + self.duty() + self.warehouse_fee +
                 self.last_mile + self.ad_cost_per_order +
                 self.return_rate * self.return_cost)
        return fixed / (1 - self.commission_rate)

    def max_affordable_cpa(self, target_margin: float = 0.15) -> float:
        """Largest ad cost per order that still hits the target net margin."""
        target_profit = self.selling_price * target_margin
        other = (self.landed_cost() + self.duty() + self.warehouse_fee +
                 self.last_mile + self.selling_price * self.commission_rate +
                 self.return_rate * self.return_cost)
        return self.selling_price - target_profit - other

    def report(self) -> str:
        lines = [
            f"  selling price          {self.selling_price:>9.2f}",
            f"  - COGS                 {self.cogs:>9.2f}",
            f"  - first-mile freight   {self.first_mile:>9.2f}",
            f"  - duty / VAT ({self.duty_rate:.0%})     {self.duty():>9.2f}",
            f"  - warehouse + lastmile {self.warehouse_fee + self.last_mile:>9.2f}",
            f"  - commission ({self.commission_rate:.1%})   {self.selling_price * self.commission_rate:>9.2f}",
            f"  - ad cost per order    {self.ad_cost_per_order:>9.2f}",
            f"  - return loss ({self.return_rate:.0%})   {self.return_rate * self.return_cost:>9.2f}",
            f"  = net profit           {self.net_profit():>9.2f}   ({self.net_margin():.1%})",
            f"  gross margin (no ad)   {self.gross_margin():>9.1%}",
            f"  break-even price       {self.breakeven_price():>9.2f}",
            f"  max CPA @15% margin    {self.max_affordable_cpa():>9.2f}",
        ]
        return "\n".join(lines)


# --------------------------------------------------------------------------- #
# 2. Inventory: safety stock, ROP, EOQ
# --------------------------------------------------------------------------- #
def safety_stock(z: float, lead_time_days: float, sigma_daily: float,
                 avg_daily: float, sigma_lead_time: float) -> float:
    """SS = z * sqrt(LT * sigma_d^2 + d^2 * sigma_LT^2)"""
    return z * math.sqrt(lead_time_days * sigma_daily ** 2 +
                         (avg_daily ** 2) * (sigma_lead_time ** 2))


def reorder_point(avg_daily: float, lead_time_days: float, ss: float) -> float:
    return avg_daily * lead_time_days + ss


def eoq(annual_demand: float, order_cost: float, unit_cost: float,
        holding_rate: float) -> float:
    """EOQ = sqrt(2 * D * S / (H)), H = unit_cost * holding_rate."""
    holding = unit_cost * holding_rate
    return math.sqrt(2 * annual_demand * order_cost / holding)


def main() -> None:
    print("=" * 74)
    print("1) UNIT ECONOMICS  (illustrative numbers, verify real fees yourself)")
    print("=" * 74)
    sku = Sku(
        name="wireless earbuds",
        selling_price=39.90, cogs=7.80, first_mile=1.60, duty_rate=0.075,
        warehouse_fee=1.35, last_mile=4.90, commission_rate=0.15,
        ad_cost_per_order=9.50, return_rate=0.08, return_cost=6.50,
    )
    print(f"SKU: {sku.name}")
    print(sku.report())

    print("\n--- sensitivity: ad cost per order ---")
    for cpa in [4.0, 6.0, 8.0, 9.5, 12.0, 15.0]:
        sku.ad_cost_per_order = cpa
        flag = "OK " if sku.net_profit() > 0 else "LOSS"
        print(f"  CPA {cpa:>5.2f} -> net profit {sku.net_profit():>7.2f} "
              f"({sku.net_margin():>6.1%})  {flag}")
    sku.ad_cost_per_order = 9.50

    print("\n--- sensitivity: return rate ---")
    for rr in [0.02, 0.05, 0.08, 0.12, 0.20]:
        sku.return_rate = rr
        print(f"  return rate {rr:>5.1%} -> net profit {sku.net_profit():>7.2f} "
              f"({sku.net_margin():>6.1%})")

    print("\n" + "=" * 74)
    print("2) INVENTORY: safety stock / ROP / EOQ")
    print("=" * 74)
    avg_daily, sigma_daily = 120.0, 35.0
    lt_days, sigma_lt = 30.0, 6.0
    for service_level, z in [("90%", 1.28), ("95%", 1.65), ("98%", 2.05), ("99%", 2.33)]:
        ss = safety_stock(z, lt_days, sigma_daily, avg_daily, sigma_lt)
        rop = reorder_point(avg_daily, lt_days, ss)
        print(f"  service {service_level:>4} (z={z:4.2f}) -> SS {ss:>7.1f} units, "
              f"ROP {rop:>7.1f} units  (pipeline demand {avg_daily * lt_days:.0f})")

    d_annual, order_cost, unit_cost, hold_rate = 120 * 365, 260.0, 7.80, 0.22
    q = eoq(d_annual, order_cost, unit_cost, hold_rate)
    print(f"\n  annual demand {d_annual:,.0f} units, order cost {order_cost:.0f}, "
          f"unit cost {unit_cost:.2f}, holding rate {hold_rate:.0%}")
    print(f"  EOQ = {q:,.1f} units -> {d_annual / q:.1f} orders/year, "
          f"cycle {365 / (d_annual / q):.1f} days")


if __name__ == "__main__":
    main()
