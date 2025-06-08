# Equipment Replacement Planner

This repository provides a simple simulation for planning the replacement of communication equipment on a cellular network. It generates random sites, estimates distances and calculates the required crews and costs for several scenarios.

## Requirements

- Python 3.10+
- `numpy`
- `streamlit` (for the dashboard)

Install the dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the planning script for all four scenarios:

```bash
python run_planning.py
```

Launch the interactive dashboard:

```bash
streamlit run dashboard.py
```

Parameters such as wages, object count, and road type can be adjusted through the dashboard or by editing `planner.Config` in the scripts.
