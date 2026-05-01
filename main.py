# main.py
from simulation.water_env import WaterEnvironment
from simulation.config import START_POS, TARGET_WAYPOINTS
from src.perception import Perception
from src.detector import ZoneDetector
from src.path_planner import AStarPlanner
from src.navigation import RobotNavigator
from src.visualizer import Visualizer

def main():
    env = WaterEnvironment(country="EU_Urban_Wastewater")
    perception = Perception(env)
    detector = ZoneDetector()
    robot = RobotNavigator(env, perception, detector)
    robot.set_position(*START_POS)
    planner = AStarPlanner(env)
    full_path = []
    current = START_POS
    waypoints = list(TARGET_WAYPOINTS)
    while waypoints:
        nearest = min(waypoints, key=lambda wp: planner.heuristic(current, wp))
        seg = planner.plan(current, nearest)
        if seg:
            if full_path and seg[0] == full_path[-1]:
                seg = seg[1:]
            full_path.extend(seg)
            current = nearest
        waypoints.remove(nearest)
    if not full_path:
        print("No path found")
        return
    viz = Visualizer(env, robot)
    viz.run(full_path)
    robot.save_log()

if __name__ == "__main__":
    main()
