def load_parameters(scenario=None):
    """
    Loads all necessary parameters for the optimization model.
    Allows for scenario testing by modifying parameters based on the scenario argument.
    """
    params = {
        'factories': ['Rayong', 'Ayutthaya', 'Chiang Mai', 'Hat Yai'],
        'products': ['Jasmine Rice', 'Processed Seafood', 'Rubber', 'Palm Oil'],
        'production_cost': {
            'Rayong': {'Jasmine Rice': 150, 'Processed Seafood': 200, 'Rubber': 250, 'Palm Oil': 180},
            'Ayutthaya': {'Jasmine Rice': 140, 'Processed Seafood': 210, 'Rubber': 260, 'Palm Oil': 175},
            'Chiang Mai': {'Jasmine Rice': 160, 'Processed Seafood': 220, 'Rubber': 270, 'Palm Oil': 185},
            'Hat Yai': {'Jasmine Rice': 155, 'Processed Seafood': 205, 'Rubber': 255, 'Palm Oil': 190},
        },
        'capacity': {
            'Rayong': 10000,
            'Ayutthaya': 15000,
            'Chiang Mai': 8000,
            'Hat Yai': 12000,
        },
        'demand': {
            'Singapore': 12000,
            'Kuala Lumpur': 8000,
            'Jakarta': 7500,
            'Ho Chi Minh City': 10000,
            'Manila': 9000
        },
        'product_demand': {
            'Jasmine Rice': 12000,
            'Processed Seafood': 8000,
            'Rubber': 7500,
            'Palm Oil': 10000
        },
        'transport_cost': {
            'Laem Chabang': {
                'Singapore': {'Road': 0.12, 'Ocean': 0.05, 'Air': 1.20},
                'Kuala Lumpur': {'Road': 0.10, 'Ocean': 0.04, 'Air': 1.10},
                'Jakarta': {'Road': 0.15, 'Ocean': 0.06, 'Air': 1.30},
                'Ho Chi Minh City': {'Road': 0.09, 'Ocean': 0.04, 'Air': 1.15},
                'Manila': {'Road': 0.14, 'Ocean': 0.07, 'Air': 1.40}
            },
            'Lat Krabang': {
                'Singapore': {'Road': 0.11, 'Ocean': 0.05, 'Air': 1.18},
                'Kuala Lumpur': {'Road': 0.09, 'Ocean': 0.04, 'Air': 1.08},
                'Jakarta': {'Road': 0.14, 'Ocean': 0.06, 'Air': 1.28},
                'Ho Chi Minh City': {'Road': 0.08, 'Ocean': 0.04, 'Air': 1.12},
                'Manila': {'Road': 0.13, 'Ocean': 0.07, 'Air': 1.38}
            }
        },
        'storage_cost': {
            'Laem Chabang': 5,
            'Lat Krabang': 4
        },
        'mode_capacity': {
            'Laem Chabang': {'Road': 5000, 'Ocean': 20000, 'Air': 2000},
            'Lat Krabang': {'Road': 4000, 'Ocean': 15000, 'Air': 1500}
        },
        'hub_capacity': {
            'Laem Chabang': 50000,
            'Lat Krabang': 30000
        },
        'transit_time': {
            'Laem Chabang': {
                'Singapore': {'Road': 3, 'Ocean': 5, 'Air': 1},
                'Kuala Lumpur': {'Road': 2, 'Ocean': 4, 'Air': 1},
                'Jakarta': {'Road': 4, 'Ocean': 6, 'Air': 2},
                'Ho Chi Minh City': {'Road': 2, 'Ocean': 4, 'Air': 1},
                'Manila': {'Road': 5, 'Ocean': 7, 'Air': 2}
            },
            'Lat Krabang': {
                'Singapore': {'Road': 3, 'Ocean': 5, 'Air': 1},
                'Kuala Lumpur': {'Road': 2, 'Ocean': 4, 'Air': 1},
                'Jakarta': {'Road': 4, 'Ocean': 6, 'Air': 2},
                'Ho Chi Minh City': {'Road': 2, 'Ocean': 4, 'Air': 1},
                'Manila': {'Road': 5, 'Ocean': 7, 'Air': 2}
            }
        },
        'carbon_emission': {
            'Laem Chabang': {
                'Singapore': {'Road': 62, 'Ocean': 16, 'Air': 500},
                'Kuala Lumpur': {'Road': 60, 'Ocean': 14, 'Air': 480},
                'Jakarta': {'Road': 65, 'Ocean': 18, 'Air': 520},
                'Ho Chi Minh City': {'Road': 58, 'Ocean': 14, 'Air': 490},
                'Manila': {'Road': 70, 'Ocean': 20, 'Air': 530}
            },
            'Lat Krabang': {  # ✅ Add Lat Krabang emissions
                'Singapore': {'Road': 61, 'Ocean': 15, 'Air': 490},
                'Kuala Lumpur': {'Road': 59, 'Ocean': 13, 'Air': 470},
                'Jakarta': {'Road': 64, 'Ocean': 17, 'Air': 510},
                'Ho Chi Minh City': {'Road': 57, 'Ocean': 13, 'Air': 480},
                'Manila': {'Road': 69, 'Ocean': 19, 'Air': 520}
            }
        },
        'tariffs': {
            'Singapore': 20,
            'Kuala Lumpur': 15,
            'Jakarta': 25,
            'Ho Chi Minh City': 18,
            'Manila': 22
        },
        'max_delivery_time': 7
    }

    # Apply Fuel Price Surge Scenario
    if scenario == 'fuel_surge':
        for hub in params['transport_cost']:
            for dest in params['transport_cost'][hub]:
                params['transport_cost'][hub][dest]['Road'] *= 1.3  # Increase road costs by 30%
                params['transport_cost'][hub][dest]['Air'] *= 1.3  # Increase air costs by 30%

    return params
