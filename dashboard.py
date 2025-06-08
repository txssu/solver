#!/usr/bin/env python3
"""Streamlit dashboard for logistic planning."""
import streamlit as st
from solver import planner

st.title("Equipment Replacement Planner")

network_type = st.selectbox("Network type", ["star", "spider"])
warehouses = st.slider("Warehouses", 1, 4, 1)
num_objects = st.number_input("Number of objects", 100, 2000, 1000)
months = st.select_slider("Timeframe (months)", [2, 3, 4], value=2)

cfg = planner.Config(num_objects=num_objects, network_type=network_type, warehouses=warehouses)

result = planner.solve_scenario(cfg, months)

st.subheader("Results")
st.write(result)
