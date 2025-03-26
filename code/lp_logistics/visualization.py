import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
import pandas as pd
import geopandas as gpd
import contextily as ctx

def plot_cost_comparison(results_summary):
    scenarios = results_summary.columns[1:]
    production_costs = results_summary.loc[
        results_summary["Metric"] == "Total Production Cost ($M)", scenarios].values.flatten()
    transport_costs = results_summary.loc[
        results_summary["Metric"] == "Total Transport Cost ($M)", scenarios].values.flatten()
    storage_costs = results_summary.loc[
        results_summary["Metric"] == "Total Storage Cost ($M)", scenarios].values.flatten()

    production_costs = production_costs.astype(float)
    transport_costs = transport_costs.astype(float)
    storage_costs = storage_costs.astype(float)

    total_costs = production_costs + transport_costs + storage_costs

    production_percent = (production_costs / total_costs) * 100
    transport_percent = (transport_costs / total_costs) * 100
    storage_percent = (storage_costs / total_costs) * 100

    x = np.arange(len(scenarios))
    width = 0.5

    fig, ax = plt.subplots(figsize=(9, 6))  
    bars1 = ax.bar(x, production_costs, width, label='Production Cost', color='#1f77b4')
    bars2 = ax.bar(x, transport_costs, width, bottom=production_costs, label='Transport Cost', color='#ff7f0e')
    bars3 = ax.bar(x, storage_costs, width, bottom=production_costs + transport_costs, label='Storage Cost', color='#2ca02c')

    ax.set_xlabel("Scenario", fontsize=12)
    ax.set_ylabel("Total Cost (Million $)", fontsize=12)
    ax.set_title("Comparison of Total Costs Across Scenarios", fontsize=14)
    ax.set_xticks(x)
    ax.set_xticklabels(scenarios, fontsize=10)
    ax.legend(loc='upper left', bbox_to_anchor=(1, 1), fontsize=10)

    for i in range(len(scenarios)):
        ax.text(x[i], production_costs[i] / 2, f"{production_percent[i]:.1f}%", ha='center', va='center', color='white', fontsize=10)
        ax.text(x[i], production_costs[i] + transport_costs[i] / 2, f"{transport_percent[i]:.1f}%", ha='center', va='center', color='white', fontsize=10)
        ax.text(x[i], production_costs[i] + transport_costs[i] + storage_costs[i] / 2, f"{storage_percent[i]:.1f}%", ha='center', va='center', color='white', fontsize=10)
        ax.text(x[i], total_costs[i] + 0.05, f"Total: ${total_costs[i]:.2f}M", ha='center', va='bottom', fontsize=11, fontweight='bold')

    plt.tight_layout()
    plt.show()

def plot_transport_modes(destinations, modes, mode_volumes, transport_costs, carbon_emissions):

    mode_volumes = np.maximum(0, mode_volumes)  
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    x = np.arange(len(destinations))
    width = 0.25

    for i, mode in enumerate(modes):
        ax1.bar(x + width * (i - 1), mode_volumes[:, i], width, label=mode)

    ax1.set_ylabel('Volume (tons)')
    ax1.set_title('Transport Mode Selection by Destination')
    ax1.set_xticks(x)
    ax1.set_xticklabels(destinations)
    ax1.legend()

    if transport_costs and carbon_emissions:
        cost_ocean = [transport_costs[dest]['Ocean'] for dest in destinations]
        emissions_ocean = [carbon_emissions[dest]['Ocean'] for dest in destinations]
        cost_road = [transport_costs[dest]['Road'] for dest in destinations]
        emissions_road = [carbon_emissions[dest]['Road'] for dest in destinations]
        cost_air = [transport_costs[dest]['Air'] for dest in destinations]
        emissions_air = [carbon_emissions[dest]['Air'] for dest in destinations]

        ax2.scatter(emissions_ocean, cost_ocean, s=100, c='blue', label='Ocean', alpha=0.7)
        ax2.scatter(emissions_road, cost_road, s=100, c='green', label='Road', alpha=0.7)
        ax2.scatter(emissions_air, cost_air, s=100, c='red', label='Air', alpha=0.7)

        for i, dest in enumerate(destinations):
            ax2.annotate(dest, (emissions_ocean[i], cost_ocean[i]), xytext=(5, 5), textcoords='offset points')

        ax2.set_xlabel('Carbon Emissions (kg CO2 per ton)')
        ax2.set_ylabel('Transport Cost ($ per ton-km)')
        ax2.set_title('Transport Mode Selection: Cost vs. Emissions')
        ax2.grid(True, linestyle='--', alpha=0.7)
        ax2.legend()

    plt.tight_layout()
    plt.savefig('transport_mode_selection.png', dpi=300, bbox_inches='tight')
    plt.show()


def plot_production_allocation(factory_production_plan, factory_capacities):
    factories = list(set(f for f, p in factory_production_plan.keys()))
    products = list(set(p for f, p in factory_production_plan.keys()))
    production_dict = {f: {p: factory_production_plan.get((f, p), 0) for p in products} for f in factories}
    production_data = np.array([
        [production_dict[f][p] for p in products] for f in factories
    ])
    capacities = [factory_capacities[f] for f in factories]

    fig, ax = plt.subplots(figsize=(10, 6))
    bottom = np.zeros(len(factories))

    for i, product in enumerate(products):
        product_data = production_data[:, i]
        ax.bar(factories, product_data, bottom=bottom, label=product)
        bottom += product_data

    for i, factory in enumerate(factories):
        ax.hlines(y=capacities[i], xmin=i - 0.4, xmax=i + 0.4, colors='red', linestyles='dashed', linewidth=2)
        ax.text(i, capacities[i] + 300, f'Capacity: {capacities[i]}', ha='center')
        total_production = sum(production_data[i])
        utilization = (total_production / capacities[i]) * 100 if capacities[i] > 0 else 0
        ax.text(i, total_production / 2, f'{utilization:.1f}%', ha='center', va='center', fontweight='bold')

    ax.set_ylabel('Production Volume (tons)')
    ax.set_title('Production Allocation and Capacity Utilization by Facility')
    ax.legend(title='Products', loc='upper left', bbox_to_anchor=(1, 1))

    plt.tight_layout()
    plt.savefig('production_allocation.png', dpi=300, bbox_inches='tight')
    plt.show()

def plot_sankey_transport(transshipment_plan):
    sources, targets, values, labels = [], [], [], []
    hubs = set()

    for (hub, destination, mode), quantity in transshipment_plan.items():
        if quantity > 0:
            sources.append(hub)
            targets.append(destination + " (" + mode + ")")
            values.append(quantity)
            hubs.add(hub)
    labels = list(hubs) + [t for t in targets]
    node_indices = {name: i for i, name in enumerate(labels)}
    source_indices = [node_indices[s] for s in sources]
    target_indices = [node_indices[t] for t in targets]

    fig = go.Figure(go.Sankey(
        node=dict(label=labels, pad=15, thickness=20),
        link=dict(source=source_indices, target=target_indices, value=values)
    ))

    fig.update_layout(title_text="Transport Flow Sankey Diagram", font_size=12)
    fig.show()


def plot_geo_transport(transshipment_plan):
    """
    Plots transport routes on a map using GeoPandas with an external shapefile.
    """
    world = gpd.read_file("https://naturalearth.s3.amazonaws.com/110m_cultural/ne_110m_admin_0_countries.zip")

    fig, ax = plt.subplots(figsize=(10, 6))
    world.to_crs(epsg=3857).plot(ax=ax, color="lightgrey")

    locations = {
        "Laem Chabang": (100.9, 13.1), "Lat Krabang": (101.0, 13.7),
        "Singapore": (103.8, 1.3), "Kuala Lumpur": (101.7, 3.1),
        "Jakarta": (106.8, -6.2), "Ho Chi Minh City": (106.7, 10.8),
        "Manila": (121.0, 14.6)
    }

    for (hub, destination, mode), quantity in transshipment_plan.items():
        if quantity > 0:
            x_values = [locations[hub][0], locations[destination][0]]
            y_values = [locations[hub][1], locations[destination][1]]
            ax.plot(x_values, y_values, marker="o", label=f"{hub} → {destination} ({mode}): {quantity} tons")

    ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik)
    plt.legend()
    plt.title("Geographic Transport Flow")
    plt.show()

def plot_geo_routes(transshipment_plan): # Comment this out if it takes too long _> just a map for my report visuals not a main analysis.
    locations = {
        "Laem Chabang": [13.0878, 100.8930],
        "Lat Krabang": [13.7234, 100.7825],
        "Singapore": [1.3521, 103.8198],
        "Kuala Lumpur": [3.1390, 101.6869],
        "Jakarta": [-6.2088, 106.8456],
        "Ho Chi Minh City": [10.7769, 106.7009],
        "Manila": [14.5995, 120.9842]
    }

    fig = go.Figure()

    for (hub, dest, mode), quantity in transshipment_plan.items():
        if quantity > 0:
            fig.add_trace(go.Scattergeo(
                lon=[locations[hub][1], locations[dest][1]],
                lat=[locations[hub][0], locations[dest][0]],
                mode='lines',
                line=dict(width=2, color='blue')
            ))

    fig.update_layout(
        title="Optimized Transport Routes",
        geo=dict(
            showcoastlines=True,
            projection_type="natural earth",
            showcountries=True,
            lataxis=dict(range=[-10, 25]), 
            lonaxis=dict(range=[95, 130])  
        ),
        showlegend=False 
    )

    fig.show()
    fig.write_html("supply_chain_map.html", include_plotlyjs='cdn')
