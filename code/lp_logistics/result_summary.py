import pandas as pd
def summarize_results(production_costs_baseline, production_costs_fuel_surge,
                      transport_cost_baseline, transport_cost_fuel_surge,
                      storage_cost_baseline, storage_cost_fuel_surge,
                      fixed_transport_cost, fixed_storage_cost):
    transport_savings = (fixed_transport_cost - transport_cost_fuel_surge) / fixed_transport_cost * 100
    storage_savings = (fixed_storage_cost - storage_cost_fuel_surge) / fixed_storage_cost * 100

    data = {
        "Metric": [
            "Total Production Cost ($M)",
            "Total Transport Cost ($M)",
            "Total Storage Cost ($M)",
            "Cost Savings from Optimization (%)"
        ],
        "Baseline": [
            production_costs_baseline,
            transport_cost_baseline,
            storage_cost_baseline,
            "-"
        ],
        "Fuel Surge (Fixed Logistics)": [
            production_costs_fuel_surge,
            fixed_transport_cost,
            fixed_storage_cost,
            "-"
        ],
        "Fuel Surge (Optimized)": [
            production_costs_fuel_surge,
            transport_cost_fuel_surge,
            storage_cost_fuel_surge,
            f"Transport: {transport_savings:.2f}%, Storage: {storage_savings:.2f}%"
        ]
    }

    df_summary = pd.DataFrame(data)
    return df_summary