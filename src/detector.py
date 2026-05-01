# src/detector.py
from simulation.config import GRID_SIZE  # not used, but kept for consistency

class ZoneDetector:
    @staticmethod
    def classify_water(water_data):
        if water_data is None:
            return "Obstacle"
        # Simple classification (you can extend)
        if water_data['nitrate_ppm'] > 10:
            return "Eutrophication Risk"
        return "Safe"
    
    @staticmethod
    def is_sampling_target(water_data):
        if water_data is None:
            return False
        return water_data['nitrate_ppm'] > 10
