#!/usr/bin/env python3
"""Run logistic planning for multiple scenarios."""
from solver import planner

SCENARIOS = [
    {"name": "Weak roads, 1 warehouse", "network_type": "star", "warehouses": 1},
    {"name": "Weak roads, 4 warehouses", "network_type": "star", "warehouses": 4},
    {"name": "Developed roads, 1 warehouse", "network_type": "spider", "warehouses": 1},
    {"name": "Developed roads, 4 warehouses", "network_type": "spider", "warehouses": 4},
]

MONTHS_OPTIONS = [2, 3, 4]


def main():
    for sc in SCENARIOS:
        print("Scenario:", sc["name"])
        cfg = planner.Config(network_type=sc["network_type"], warehouses=sc["warehouses"])
        for months in MONTHS_OPTIONS:
            res = planner.solve_scenario(cfg, months)
            print(f"  {months} months -> crews: {res['crews']}, total cost: {res['total']:.2f}")
        print()


if __name__ == "__main__":
    main()
