# -*- coding: utf-8 -*-
"""Модуль планирования логистики замены оборудования."""

from dataclasses import dataclass, field
from typing import List, Tuple
import numpy as np

@dataclass
class Config:
    num_objects: int = 1000
    regional_centers: List[Tuple[float, float]] = field(default_factory=lambda: [(0,0),(100,0),(0,100),(100,100)])
    network_type: str = "star"  # "star" или "spider"
    warehouses: int = 1
    working_hours: int = 10  # часов в день
    replace_minutes: int = 70
    car_capacity: int = 16
    speed_kmh: int = 50
    car_cost_per_day: float = 8000
    engineer_salary: float = 80000
    driver_salary: float = 65000
    hotel_cost: float = 2000
    allowance_cost: float = 1000


def generate_objects(cfg: Config):
    """Случайным образом формирует координаты объектов."""
    rng = np.random.default_rng(0)
    centers = np.array(cfg.regional_centers)
    objects = []
    for i in range(cfg.num_objects):
        idx = rng.integers(0, len(centers))
        center = centers[idx]
        offset = rng.normal(scale=20, size=2)
        objects.append(center + offset)
    return np.array(objects)


def distance(a, b):
    """Евклидово расстояние между двумя точками."""
    return np.linalg.norm(a - b)


def distance_matrix(points):
    """Матрица попарных расстояний."""
    n = len(points)
    mat = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            d = distance(points[i], points[j])
            mat[i, j] = mat[j, i] = d
    return mat


def objects_per_day(cfg: Config, avg_distance_km: float):
    """Сколько объектов может обработать одна бригада за день."""
    travel_minutes = (avg_distance_km * 2 / cfg.speed_kmh) * 60
    total_minutes = cfg.replace_minutes + travel_minutes
    max_objects = (cfg.working_hours * 60) // total_minutes
    return int(min(cfg.car_capacity, max_objects))


def required_crews(cfg: Config, months: int, avg_distance_km: float):
    """Подсчёт необходимого количества бригад."""
    objs_day = objects_per_day(cfg, avg_distance_km)
    if objs_day == 0:
        return float('inf')
    capacity = objs_day * months * 30
    crews = int(np.ceil(cfg.num_objects / capacity))
    return max(crews, 1)


def cost_estimate(cfg: Config, months: int, avg_distance_km: float):
    """Расчёт стоимости сценария."""
    crews = required_crews(cfg, months, avg_distance_km)
    days = months * 30
    wages = crews * (cfg.engineer_salary + cfg.driver_salary) * (months / 1)
    cars = crews * cfg.car_cost_per_day * days
    hotels = crews * cfg.hotel_cost * days
    allowance = crews * cfg.allowance_cost * days
    return {
        'бригады': crews,
        'зарплата': wages,
        'автомобили': cars,
        'гостиницы': hotels,
        'командировочные': allowance,
        'итого': wages + cars + hotels + allowance,
    }



def assign_objects_to_centers(objects, cfg: Config):
    """Назначает каждый объект ближайшему региональному центру."""
    centers = np.array(cfg.regional_centers)
    assignments = []
    for obj in objects:
        dists = np.linalg.norm(centers - obj, axis=1)
        assignments.append(np.argmin(dists))
    return np.array(assignments)


def average_distance(objects, assignments, cfg: Config):
    """Среднее расстояние от объектов до складов/центров."""
    centers = np.array(cfg.regional_centers)
    factor = 1.3 if cfg.network_type == "star" else 1.0
    if cfg.warehouses == 1:
        wh = centers[0]
        dists = np.linalg.norm(objects - wh, axis=1) * factor
        return float(np.mean(dists))
    total = 0.0
    for center_idx in range(len(centers)):
        idxs = np.where(assignments == center_idx)[0]
        if len(idxs) == 0:
            continue
        dist = np.linalg.norm(objects[idxs] - centers[center_idx], axis=1) * factor
        total += np.sum(dist)
    return total / len(objects)


def solve_scenario(cfg: Config, months: int):
    """Полный расчёт одного сценария."""
    objects = generate_objects(cfg)
    assignments = assign_objects_to_centers(objects, cfg)
    avg_dist = average_distance(objects, assignments, cfg)
    result = cost_estimate(cfg, months, avg_dist)
    return result


def scenario_table(cfg: Config, months_options: List[int]) -> List[dict]:
    """Вычисляет результаты для набора сроков выполнения."""
    rows = []
    for m in months_options:
        res = solve_scenario(cfg, m)
        rows.append({
            'network_type': cfg.network_type,
            'warehouses': cfg.warehouses,
            'months': m,
            **res,
        })
    return rows


def run_variants(months_options: List[int]) -> List[dict]:
    """Запускает все четыре обязательных сценария."""
    rows = []
    for net in ['star', 'spider']:
        for wh in [1, 4]:
            cfg = Config(network_type=net, warehouses=wh)
            rows.extend(scenario_table(cfg, months_options))
    return rows


def generate_report(results: List[dict]) -> str:
    """Формирует текстовый технико-экономический отчёт."""
    lines = ["# Технико-экономический отчёт", ""]
    scenario_names = {
        ('star', 1): 'Слабая сеть дорог, 1 склад',
        ('star', 4): 'Слабая сеть дорог, 4 склада',
        ('spider', 1): 'Развитая сеть дорог, 1 склад',
        ('spider', 4): 'Развитая сеть дорог, 4 склада',
    }
    for (net, wh), group in _group_by(results, ('network_type', 'warehouses')).items():
        lines.append(f"## {scenario_names[(net, wh)]}")
        for row in sorted(group, key=lambda r: r['months']):
            lines.append(
                f"- {row['months']} мес.: бригады {row['бригады']}, итог {row['итого']:.2f} руб."
            )
        lines.append("")
    heur = derive_heuristics(results)
    lines.append("## Выводы")
    for h in heur:
        lines.append(f"- {h}")
    return "\n".join(lines)


def _group_by(rows: List[dict], keys: Tuple[str, ...]) -> dict:
    grouped = {}
    for row in rows:
        k = tuple(row[k] for k in keys)
        grouped.setdefault(k, []).append(row)
    return grouped


def derive_heuristics(results: List[dict]) -> List[str]:
    """Выводит эвристические правила по результатам расчётов."""
    heuristics = []

    # Сравнение сроков
    for months in [2, 3, 4]:
        costs = [r['итого'] for r in results if r['months'] == months]
        if months > 2 and costs and min(costs) < max(costs):
            heuristics.append(
                "увеличение срока работ снижает количество бригад и суммарную стоимость"
            )
            break

    # Больше складов против одного
    for net in ['star', 'spider']:
        pair = [r for r in results if r['network_type'] == net and r['months'] == 2]
        c1 = next((r for r in pair if r['warehouses'] == 1), None)
        c4 = next((r for r in pair if r['warehouses'] == 4), None)
        if c1 and c4 and c4['итого'] < c1['итого']:
            heuristics.append(
                "увеличение числа складов сокращает расходы на перевозки и стоимость"
            )
            break

    # Звезда против паутины
    pair_star = [r for r in results if r['network_type'] == 'star' and r['months'] == 2]
    pair_spider = [r for r in results if r['network_type'] == 'spider' and r['months'] == 2]
    for wh in [1, 4]:
        r_star = next((r for r in pair_star if r['warehouses'] == wh), None)
        r_spider = next((r for r in pair_spider if r['warehouses'] == wh), None)
        if r_star and r_spider and r_spider['итого'] < r_star['итого']:
            heuristics.append(
                "развитая дорожная сеть (\"паутина\") уменьшает расстояния и издержки"
            )
            break

    return heuristics

