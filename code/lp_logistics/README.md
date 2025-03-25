# 🚢 LP_Logistics: Multi-Stage Linear Programming for Southeast Asia Supply Chain Optimization

This project applies a two-stage linear programming approach to optimize an agricultural export company's supply chain network across Southeast Asia. It focuses on minimizing costs across production, domestic transportation, and international shipping while incorporating real-world constraints like capacity limits and carbon emissions.

---

## Project Overview

The solution is broken into **two sequential optimization models**:

1. **Stage 1 – Production Optimization** (`factory.py`)  
   - Determines optimal production quantities across four manufacturing facilities in Thailand.
   - Considers production costs, demand satisfaction, and capacity constraints.

2. **Stage 2 – Transportation Optimization** (`transshipment.py`)  
   - Optimizes flow from plants to intermodal hubs and onward to international markets.
   - Minimizes transport costs while factoring in hub capacities, modal constraints, and emission limits.

Both stages are implemented using **linear programming** and executed via a modular architecture.

---

## File Structure

| File/Folder                 | Description |
|----------------------------|-------------|
| `main.py`                  | Main script — runs the complete pipeline (both models + visualization + output). |
| `config2.py`               | Contains all configurable parameter values (e.g., costs, capacities, emissions). |
| `factory.py`               | Stage 1 model — optimizes production allocation. |
| `transshipment.py`         | Stage 2 model — optimizes routing and mode selection. |
| `visualization.py`         | Contains transport mode visualization and mapping logic. |
| `cost_comparison.py`       | Compares total logistics cost under different scenarios. |
| `result_summary.py`        | Extracts and formats optimization results into final summary. |


---

## Requirements

Install dependencies using `pip`:

```bash
pip install -r requirements.txt
```

## Outcomes

transport_mode_selection.png — Shows how products are shipped using different transport modes

production_allocation.png — Factory output decisions

supply_chain_map.html — Interactive map of the full logistics network

supply_chain_summary.csv — Final optimization result summary

cost_comparison.py — Optional cost sensitivity scenarios (e.g., fuel price shock)