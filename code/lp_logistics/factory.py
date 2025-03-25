import pulp
from config2 import load_parameters

def optimize_factory_production():
    params = load_parameters()
    factories = params['factories'] 
    products = params['products']  
    production_cost = params['production_cost']  
    capacity = params['capacity']  
    demand = params['product_demand']  
    hub_capacity = params['hub_capacity']  

    model = pulp.LpProblem("Factory_Production_Optimization", pulp.LpMinimize)

    production_vars = {
        (f, p): pulp.LpVariable(f"Production_{f}_{p}", lowBound=0, cat='Continuous')
        for f in factories for p in products
    }

    # obj
    model += pulp.lpSum(production_cost[f][p] * production_vars[f, p] for f in factories for p in products)

    # Constraints
    # 1
    for f in factories:
        model += pulp.lpSum(production_vars[f, p] for p in products) <= capacity[f], f"Capacity_{f}"

    # 2
    for p in products:
        model += pulp.lpSum(production_vars[f, p] for f in factories) >= demand[p], f"Demand_{p}"

    # 3
    hub_assignment = {
        "Rayong": "Laem Chabang",
        "Hat Yai": "Laem Chabang",
        "Ayutthaya": "Lat Krabang",
        "Chiang Mai": "Lat Krabang"
    }

    hub_production = {
        h: pulp.lpSum(production_vars[f, p] for f, hub in hub_assignment.items() if hub == h for p in products)
        for h in hub_capacity}

    for h in hub_capacity:
        model += hub_production[h] <= hub_capacity[h], f"Hub_Capacity_{h}"

    model.solve()
    production_plan = {(f, p): production_vars[f, p].varValue for f in factories for p in products}
    return production_plan


if __name__ == "__main__":
    results = optimize_factory_production()
    print("Optimal Production Plan:")
    for (factory, product), quantity in results.items():
        print(f"Factory {factory} produces {quantity} tons of {product}")

