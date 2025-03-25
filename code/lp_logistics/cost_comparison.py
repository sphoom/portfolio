import pandas as pd

def calculate_fixed_logistics_cost(transshipment_plan_baseline, transport_costs_fuel_surge, storage_costs_fuel_surge):
    total_transport_cost_fixed = sum(
        transshipment_plan_baseline[(hub, dest, mode)] * transport_costs_fuel_surge[hub][dest][mode]
        for (hub, dest, mode) in transshipment_plan_baseline if transshipment_plan_baseline[(hub, dest, mode)] > 0
    ) / 1e6  
    total_storage_cost_fixed = sum(
        transshipment_plan_baseline[(hub, dest, mode)] * storage_costs_fuel_surge[hub]
        for (hub, dest, mode) in transshipment_plan_baseline if transshipment_plan_baseline[(hub, dest, mode)] > 0
    ) / 1e6 

    return total_transport_cost_fixed, total_storage_cost_fixed


def generate_transport_table(transshipment_plan):
    transport_data = []
    for (hub, destination, mode), quantity in transshipment_plan.items():
        if quantity > 0:  
            transport_data.append([hub, destination, mode, round(quantity, 2)])

    df_transport = pd.DataFrame(transport_data, columns=["Origin Hub", "Destination", "Transport Mode", "Volume (tons)"])
    df_transport.to_csv("tables/transport_summary.csv", index=False) 
    print("\nTransport Flow Summary:")
    print(df_transport)
    return df_transport