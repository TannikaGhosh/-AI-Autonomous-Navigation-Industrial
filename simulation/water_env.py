# simulation/water_env.py
import numpy as np
from .config import GRID_SIZE, BASELINE, LANDUSE_BY_COUNTRY

class WaterEnvironment:
    def __init__(self, country="EU_Urban_Wastewater"):
        self.grid_size = GRID_SIZE
        self.country = country
        self.obstacles = np.zeros((GRID_SIZE, GRID_SIZE), dtype=bool)
        
        self.params = {}
        for key, val in BASELINE.items():
            self.params[key] = np.ones((GRID_SIZE, GRID_SIZE)) * val
        
        self._setup_obstacles()
        self._setup_water_quality()
    
    def _setup_obstacles(self):
        # Central island
        for i in range(8, 12):
            for j in range(8, 12):
                self.obstacles[i][j] = True
        # Random rocks
        np.random.seed(42)
        for _ in range(12):
            x = np.random.randint(0, GRID_SIZE)
            y = np.random.randint(0, GRID_SIZE)
            if not (8 <= x < 12 and 8 <= y < 12):
                self.obstacles[x][y] = True
    
    def _setup_water_quality(self):
        landuse_dict = LANDUSE_BY_COUNTRY.get(self.country, {})
        for landuse, props in landuse_dict.items():
            x1, y1, x2, y2 = props["rect"]
            for i in range(x1, min(x2+1, self.grid_size)):
                for j in range(y1, min(y2+1, self.grid_size)):
                    if self.obstacles[i][j]:
                        continue
                    for param, add_val in props.items():
                        if param == "rect":
                            continue
                        if param in self.params:
                            self.params[param][i][j] += add_val
        
        # Clip to realistic ranges
        self.params['nitrate_ppm'] = np.clip(self.params['nitrate_ppm'], 0, 50)
        self.params['phosphate_ugL'] = np.clip(self.params['phosphate_ugL'], 0, 30)
        self.params['temperature_c'] = np.clip(self.params['temperature_c'], 15, 35)
        self.params['ph'] = np.clip(self.params['ph'], 5.5, 9.0)
        self.params['dissolved_oxygen_mgL'] = np.clip(self.params['dissolved_oxygen_mgL'], 0, 12)
        self.params['turbidity_ntu'] = np.clip(self.params['turbidity_ntu'], 0, 100)
        self.params['bod_mgL'] = np.clip(self.params['bod_mgL'], 0, 80)
        self.params['cod_mgL'] = np.clip(self.params['cod_mgL'], 0, 400)
        self.params['lead_ugL'] = np.clip(self.params['lead_ugL'], 0, 2)
        self.params['mercury_ugL'] = np.clip(self.params['mercury_ugL'], 0, 0.5)
    
    def is_obstacle(self, x, y):
        if 0 <= x < self.grid_size and 0 <= y < self.grid_size:
            return self.obstacles[x][y]
        return True
    
    def get_water_quality(self, x, y):
        if self.is_obstacle(x, y):
            return None
        return {param: round(arr[x][y], 2) for param, arr in self.params.items()}
    
    def get_landuse_map(self):
        landuse_grid = np.full((self.grid_size, self.grid_size), "Unknown", dtype=object)
        landuse_dict = LANDUSE_BY_COUNTRY.get(self.country, {})
        for name, props in landuse_dict.items():
            x1, y1, x2, y2 = props["rect"]
            for i in range(x1, min(x2+1, self.grid_size)):
                for j in range(y1, min(y2+1, self.grid_size)):
                    if not self.is_obstacle(i, j):
                        landuse_grid[i][j] = name
        return landuse_grid
