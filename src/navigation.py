# src/navigation.py
import csv
import os
from datetime import datetime

class RobotNavigator:
    def __init__(self, environment, perception, detector):
        self.env = environment
        self.perception = perception
        self.detector = detector
        self.x = None
        self.y = None
        self.log_data = []
    
    def set_position(self, x, y):
        self.x = x
        self.y = y
        self._record_reading()
    
    def move(self, target_x, target_y):
        if abs(self.x - target_x) + abs(self.y - target_y) != 1:
            return False
        if self.env.is_obstacle(target_x, target_y):
            return False
        self.x, self.y = target_x, target_y
        self._record_reading()
        return True
    
    def _record_reading(self):
        water = self.perception.sense(self.x, self.y)
        if water:
            entry = {'timestamp': datetime.now().isoformat(), 'x': self.x, 'y': self.y}
            entry.update(water)
            entry['risk'] = self.detector.classify_water(water)
            self.log_data.append(entry)
    
    def save_log(self, filename="data/water_quality_log.csv"):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        if not self.log_data:
            return
        with open(filename, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=self.log_data[0].keys())
            writer.writeheader()
            writer.writerows(self.log_data)
        print(f"Log saved to {filename}")
