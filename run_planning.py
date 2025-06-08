#!/usr/bin/env python3
"""Запуск планировщика для нескольких сценариев."""
from solver import planner

SCENARIOS = [
    {"name": "Слабая сеть дорог, 1 склад", "network_type": "star", "warehouses": 1},
    {"name": "Слабая сеть дорог, 4 склада", "network_type": "star", "warehouses": 4},
    {"name": "Развитая сеть дорог, 1 склад", "network_type": "spider", "warehouses": 1},
    {"name": "Развитая сеть дорог, 4 склада", "network_type": "spider", "warehouses": 4},
]

MONTHS_OPTIONS = [2, 3, 4]


def main():
    for sc in SCENARIOS:
        print("Сценарий:", sc["name"])
        cfg = planner.Config(network_type=sc["network_type"], warehouses=sc["warehouses"])
        for months in MONTHS_OPTIONS:
            res = planner.solve_scenario(cfg, months)
            print(f"  {months} мес. -> бригады: {res['бригады']}, общая стоимость: {res['итого']:.2f}")
        print()


if __name__ == "__main__":
    main()
