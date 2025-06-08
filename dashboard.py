#!/usr/bin/env python3
"""Панель Streamlit для планирования."""
import streamlit as st
from solver import planner

st.title("Планировщик замены оборудования")
net_ui = st.selectbox("Тип дорожной сети", ["звезда", "паутина"])
network_type = "star" if net_ui == "звезда" else "spider"
warehouses = st.slider("Количество складов", 1, 4, 1)
num_objects = st.number_input("Количество объектов", 100, 2000, 1000)
months = st.select_slider("Срок (месяцы)", [2, 3, 4], value=2)

cfg = planner.Config(num_objects=num_objects, network_type=network_type, warehouses=warehouses)

result = planner.solve_scenario(cfg, months)

st.subheader("Результаты")
st.write(result)
