#!/usr/bin/env python3
"""Панель Streamlit для планирования."""
import streamlit as st
from solver import planner

st.title("Планировщик замены оборудования")

# основные параметры сети
net_ui = st.selectbox("Тип дорожной сети", ["звезда", "паутина"])
network_type = "star" if net_ui == "звезда" else "spider"
warehouses = st.slider("Количество складов", 1, 4, 1)
num_objects = st.number_input("Количество объектов", 100, 5000, 1000, step=100)
months = st.select_slider("Срок (месяцы)", [2, 3, 4], value=2)

# параметры работы бригады и затрат
working_hours = st.slider("Рабочий день (часы)", 8, 12, 10)
replace_minutes = st.slider("Время замены (мин)", 30, 120, 70, step=5)
car_capacity = st.number_input("Вместимость автомобиля", 1, 40, 16)
speed_kmh = st.slider("Средняя скорость (км/ч)", 30, 120, 50)
car_cost_per_day = st.number_input("Стоимость автомобиля в день", 1000, 20000, 8000, step=500)
engineer_salary = st.number_input("Зарплата инженера в месяц", 10000, 200000, 80000, step=5000)
driver_salary = st.number_input("Зарплата водителя в месяц", 10000, 200000, 65000, step=5000)
hotel_cost = st.number_input("Стоимость гостиницы", 0, 10000, 2000, step=100)
allowance_cost = st.number_input("Командировочные", 0, 10000, 1000, step=100)

cfg = planner.Config(
    num_objects=int(num_objects),
    network_type=network_type,
    warehouses=int(warehouses),
    working_hours=int(working_hours),
    replace_minutes=int(replace_minutes),
    car_capacity=int(car_capacity),
    speed_kmh=int(speed_kmh),
    car_cost_per_day=float(car_cost_per_day),
    engineer_salary=float(engineer_salary),
    driver_salary=float(driver_salary),
    hotel_cost=float(hotel_cost),
    allowance_cost=float(allowance_cost),
)

result = planner.solve_scenario(cfg, int(months))

st.subheader("Результаты")
for key, value in result.items():
    if isinstance(value, float):
        st.write(f"{key}: {value:,.2f}")
    else:
        st.write(f"{key}: {value}")
