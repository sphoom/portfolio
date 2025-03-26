from config2 import load_parameters
from factory import optimize_factory_production
from transshipment import optimize_transshipment
from visualization import plot_cost_comparison, plot_transport_modes, plot_production_allocation, plot_sankey_transport, plot_geo_transport, plot_geo_routes
from cost_comparison import calculate_fixed_logistics_cost
from result_summary import summarize_results
import pandas as pd
import numpy as np


def generate_transport_table(transshipment_plan, filename):
    transport_data = []
    for (hub, destination, mode), quantity in transshipment_plan.items():
        if quantity > 0:
            transport_data.append([hub, destination, mode, round(quantity, 2)])

    df_transport = pd.DataFrame(transport_data,
                                columns=["Origin Hub", "Destination", "Transport Mode", "Volume (tons)"])
    df_transport.to_csv(filename, index=False)
    print(f"\nTransport Flow Summary saved to {filename}")
    print(df_transport)
    return df_transport


def main():
    # Baseline Scenario
    print("Running Baseline Scenario...")
    params_baseline = load_parameters()
    factory_production_plan_baseline = optimize_factory_production()

    factory_outputs_baseline = {h: 0 for h in params_baseline['hub_capacity']}
    for f in params_baseline['factories']:
        for p in params_baseline['products']:
            assigned_hub = "Laem Chabang" if f in ["Rayong", "Hat Yai"] else "Lat Krabang"
            factory_outputs_baseline[assigned_hub] += factory_production_plan_baseline.get((f, p), 0)

    transshipment_plan_baseline = optimize_transshipment(factory_outputs_baseline)

    # Fuel Price Surge Scenario
    print("\nRunning Fuel Price Surge Scenario...")
    params_fuel_surge = load_parameters(scenario='fuel_surge')
    factory_production_plan_fuel_surge = optimize_factory_production()

    factory_outputs_fuel_surge = {h: 0 for h in params_fuel_surge['hub_capacity']}
    for f in params_fuel_surge['factories']:
        for p in params_fuel_surge['products']:
            assigned_hub = "Laem Chabang" if f in ["Rayong", "Hat Yai"] else "Lat Krabang"
            factory_outputs_fuel_surge[assigned_hub] += factory_production_plan_fuel_surge.get((f, p), 0)

    transshipment_plan_fuel_surge = optimize_transshipment(factory_outputs_fuel_surge)

    fixed_transport_cost, fixed_storage_cost = calculate_fixed_logistics_cost(
        transshipment_plan_baseline, params_fuel_surge['transport_cost'], params_fuel_surge['storage_cost']
    )


    summary_table = summarize_results(
        sum(factory_outputs_baseline.values()) * 50 / 1e6,  # cost in million
        sum(factory_outputs_fuel_surge.values()) * 50 / 1e6,
        sum(transshipment_plan_baseline[(h, d, m)] * params_baseline['transport_cost'][h][d][m]
            for (h, d, m) in transshipment_plan_baseline if transshipment_plan_baseline[(h, d, m)] > 0) / 1e6,
        sum(transshipment_plan_fuel_surge[(h, d, m)] * params_fuel_surge['transport_cost'][h][d][m]
            for (h, d, m) in transshipment_plan_fuel_surge if transshipment_plan_fuel_surge[(h, d, m)] > 0) / 1e6,
        sum(factory_outputs_baseline[h] * params_baseline['storage_cost'][h] for h in factory_outputs_baseline) / 1e6,
        sum(factory_outputs_fuel_surge[h] * params_fuel_surge['storage_cost'][h] for h in
            factory_outputs_fuel_surge) / 1e6,
        fixed_transport_cost, fixed_storage_cost
    )

    print("\nStrategic Summary:")
    print(summary_table)

    summary_table.to_csv("supply_chain_summary.csv", index=False)
    print("Results saved to supply_chain_summary.csv")

    df_transport_baseline = generate_transport_table(transshipment_plan_baseline, "transport_baseline.csv")
    df_transport_fuel_surge = generate_transport_table(transshipment_plan_fuel_surge, "transport_fuel_surge.csv")

    print("\nGenerating Cost Comparison Visualization...")
    plot_cost_comparison(summary_table)

    print("\nGenerating Production Allocation Visualization...")
    plot_production_allocation(factory_production_plan_baseline, params_baseline['capacity'])

    print("\nGenerating Geo Route Visualization...")
    plot_geo_routes(transshipment_plan_baseline)

    print("\nGenerating Transport Mode Selection Visualization...")
    destinations = list(params_baseline['demand'].keys())
    hubs = list(params_baseline['hub_capacity'].keys())
    modes = ['Road', 'Ocean', 'Air']

    aggregated_transport_costs = {
        dest: {mode: sum(params_baseline['transport_cost'][h].get(dest, {}).get(mode, 0) for h in hubs) for mode in
               modes}
        for dest in destinations
    }
    aggregated_carbon_emissions = {
        dest: {mode: sum(params_baseline['carbon_emission'][h].get(dest, {}).get(mode, 0) for h in hubs) for mode in
               modes}
        for dest in destinations
    }

    mode_volumes = np.array([
        [sum(transshipment_plan_baseline.get((h, d, m), 0) for h in hubs) for m in modes]
        for d in destinations
    ])
    plot_transport_modes(destinations, modes, mode_volumes, aggregated_transport_costs, aggregated_carbon_emissions)

    print("\nGenerating Sankey Diagram...")
    plot_sankey_transport(transshipment_plan_baseline)

    print("\nGenerating Geographic Transport Visualization...")
    plot_geo_transport(transshipment_plan_baseline)

    return summary_table


if __name__ == "__main__":
    summary_results = main()
    pd.set_option("display.float_format", "${:,.2f}".format)
    print(summary_results)



