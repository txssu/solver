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
