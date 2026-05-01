# simulation/config.py
GRID_SIZE = 20
CELL_SIZE = 30
FPS = 60

# Baseline clean water parameters
BASELINE = {
    'nitrate_ppm': 0.5,
    'phosphate_ugL': 0.5,
    'temperature_c': 20.0,
    'ph': 7.0,
    'dissolved_oxygen_mgL': 8.0,
    'turbidity_ntu': 2.0,
    'bod_mgL': 2.0,
    'cod_mgL': 10.0,
    'lead_ugL': 0.1,
    'mercury_ugL': 0.01,
}

# Land use definitions for each country
LANDUSE_EU = {
    "Farming (crops)": {
        "rect": (0, 0, 8, 12),
        "nitrate_ppm": 15,
        "phosphate_ugL": 10,
        "bod_mgL": 8,
        "cod_mgL": 30,
    },
    "Locality (town)": {
        "rect": (5, 15, 10, 19),
        "bod_mgL": 25,
        "cod_mgL": 100,
        "nitrate_ppm": 5,
        "phosphate_ugL": 6,
    },
    "Fishery (trout)": {
        "rect": (12, 0, 16, 6),
        "bod_mgL": 15,
        "dissolved_oxygen_mgL": -2,
    },
    "Poultry farm": {
        "rect": (15, 10, 19, 14),
        "bod_mgL": 50,
        "phosphate_ugL": 12,
    },
    "Data center": {
        "rect": (17, 0, 19, 4),
        "temperature_c": 8,
        "phosphate_ugL": 20,
        "lead_ugL": 0.3,
    },
    "Protected area": {
        "rect": (8, 8, 12, 12),
        "nitrate_ppm": 0.2,
        "phosphate_ugL": 0.2,
        "bod_mgL": 0.5,
    }
}

LANDUSE_INDIA = {
    "Intensive farming (rice/sugarcane)": {
        "rect": (0, 0, 10, 10),
        "nitrate_ppm": 30,
        "phosphate_ugL": 18,
        "bod_mgL": 20,
        "cod_mgL": 80,
    },
    "Dense locality (village)": {
        "rect": (5, 12, 12, 19),
        "bod_mgL": 50,
        "cod_mgL": 250,
        "dissolved_oxygen_mgL": -3,
        "phosphate_ugL": 8,
    },
    "Shrimp farm": {
        "rect": (11, 0, 15, 8),
        "bod_mgL": 40,
        "dissolved_oxygen_mgL": -3,
    },
    "Broiler poultry": {
        "rect": (13, 10, 16, 14),
        "bod_mgL": 70,
        "phosphate_ugL": 18,
    },
    "Textile factory": {
        "rect": (17, 10, 19, 16),
        "temperature_c": 12,
        "turbidity_ntu": 80,
        "cod_mgL": 350,
        "ph": -1.2,
    },
    "Chemical plant": {
        "rect": (16, 0, 19, 6),
        "nitrate_ppm": 35,
        "lead_ugL": 0.8,
        "mercury_ugL": 0.05,
        "ph": -1.5,
    }
}

LANDUSE_USA = {
    "Corporate farming (corn/soy)": {
        "rect": (0, 0, 9, 14),
        "nitrate_ppm": 18,
        "phosphate_ugL": 10,
        "bod_mgL": 10,
    },
    "Suburb": {
        "rect": (8, 15, 12, 19),
        "bod_mgL": 25,
        "cod_mgL": 90,
        "nitrate_ppm": 4,
        "phosphate_ugL": 5,
    },
    "Catfish farm": {
        "rect": (10, 0, 14, 7),
        "bod_mgL": 35,
        "dissolved_oxygen_mgL": -2.5,
    },
    "CAFO (cattle)": {
        "rect": (14, 10, 19, 15),
        "bod_mgL": 70,
        "phosphate_ugL": 18,
        "nitrate_ppm": 15,
    },
    "Data center cluster": {
        "rect": (16, 0, 19, 9),
        "temperature_c": 10,
        "phosphate_ugL": 22,
        "lead_ugL": 0.2,
    },
    "Chemical plant": {
        "rect": (5, 15, 9, 19),
        "nitrate_ppm": 25,
        "lead_ugL": 0.3,
        "ph": -0.8,
        "mercury_ugL": 0.02,
    }
}

LANDUSE_BY_COUNTRY = {
    "EU_Urban_Wastewater": LANDUSE_EU,
    "India_CPCB": LANDUSE_INDIA,
    "US_EPA_CWA": LANDUSE_USA,
    "Custom_Strict": LANDUSE_EU   # fallback
}

# No extra point sources – land use only
POLLUTION_SOURCES = {}

TARGET_WAYPOINTS = [(5,5), (15,15), (0,18), (10,10)]
START_POS = (0, 0)
