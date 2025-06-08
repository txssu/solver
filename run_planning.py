#!/usr/bin/env python3
"""Запуск планировщика для нескольких сценариев."""
from solver import planner

MONTHS_OPTIONS = [2, 3, 4]


def main():
    results = planner.run_variants(MONTHS_OPTIONS)
    scenario_names = {
        ('star', 1): 'Слабая сеть дорог, 1 склад',
        ('star', 4): 'Слабая сеть дорог, 4 склада',
        ('spider', 1): 'Развитая сеть дорог, 1 склад',
        ('spider', 4): 'Развитая сеть дорог, 4 склада',
    }

    for (net, wh), group in planner._group_by(results, ('network_type', 'warehouses')).items():
        print("Сценарий:", scenario_names[(net, wh)])
        for row in sorted(group, key=lambda r: r['months']):
            print(f"  {row['months']} мес. -> бригады: {row['бригады']}, общая стоимость: {row['итого']:.2f}")
        print()

    report_text = planner.generate_report(results)
    with open("report.md", "w", encoding="utf-8") as f:
        f.write(report_text)
    print("Отчёт сохранён в report.md")


if __name__ == "__main__":
    main()
