import pulp
from config2 import load_parameters

def optimize_transshipment(production_plan):
    """
    Optimizes transportation and distribution from Thai hubs to ASEAN distribution centers.
    Solves as a transshipment problem, enforcing hub capacity constraints strictly.
    """
    params = load_parameters()
    hubs = ['Laem Chabang', 'Lat Krabang']  
    asean_hubs = ['Singapore', 'Kuala Lumpur', 'Jakarta', 'Ho Chi Minh City', 'Manila']
    transport_modes = ['Road', 'Ocean', 'Air']

    transport_cost = params['transport_cost']  
    storage_cost = params['storage_cost']  
    demand = params['demand']  
    mode_capacity = params['mode_capacity']  
    hub_capacity = params['hub_capacity']  
    transit_time = params['transit_time']  
    carbon_emission = params['carbon_emission']  # co2 emissions per mode per ton-km
    tariffs = params['tariffs']  # tariffs per ton per ASEAN hub

    #Obj
    model = pulp.LpProblem("Transshipment_Optimization", pulp.LpMinimize)

    trans_vars = {
        (h, a, m): pulp.LpVariable(f"Transport_{h}_{a}_{m}", lowBound=0, cat='Continuous')
        for h in hubs for a in asean_hubs for m in transport_modes
    }

    model += pulp.lpSum(
        transport_cost[h][a][m] * trans_vars[h, a, m] for h in hubs for a in asean_hubs for m in transport_modes) \
             + pulp.lpSum(storage_cost[h] * production_plan[h] for h in hubs) \
             + pulp.lpSum(
        carbon_emission[h][a][m] * trans_vars[h, a, m] for h in hubs for a in asean_hubs for m in transport_modes) \
             + pulp.lpSum(
        tariffs[a] * pulp.lpSum(trans_vars[h, a, m] for h in hubs for m in transport_modes) for a in asean_hubs)

    # Constraints
    # 1
    for h in hubs:
        model += pulp.lpSum(trans_vars[h, a, m] for a in asean_hubs for m in transport_modes) >= 0, f"Flow_NonNegative_{h}"

    # 2
    for a in asean_hubs:
        model += pulp.lpSum(trans_vars[h, a, m] for h in hubs for m in transport_modes) >= demand[a], f"Demand_{a}"

    # 3
    for h in hubs:
        for m in transport_modes:
            model += pulp.lpSum(trans_vars[h, a, m] for a in asean_hubs) <= mode_capacity[h][m], f"Mode_Capacity_{h}_{m}"

    # 4.
    for h in hubs:
        model += pulp.lpSum(trans_vars[h, a, m] for a in asean_hubs for m in transport_modes) <= hub_capacity[h], f"Hub_Capacity_{h}"

    # 5
    for h in hubs:
        for a in asean_hubs:
            for m in transport_modes:
                model += trans_vars[h, a, m] * transit_time[h][a][m] <= params['max_delivery_time'], f"Time_Constraint_{h}_{a}_{m}"

    model.solve()
    transport_plan = {(h, a, m): trans_vars[h, a, m].varValue for h in hubs for a in asean_hubs for m in transport_modes}

    return transport_plan


if __name__ == "__main__":
    production_plan = {"Laem Chabang": 25000, "Lat Krabang": 30000}  # for test only -- for real call on main.py na krub
    results = optimize_transshipment(production_plan)
    print("Optimal Transport Plan:")
    for (hub, destination, mode), quantity in results.items():
        print(f"{quantity:.2f} tons from {hub} to {destination} via {mode}")
