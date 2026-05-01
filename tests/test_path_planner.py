import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from simulation.water_env import WaterEnvironment
from src.path_planner import AStarPlanner

def test_path():
    env = WaterEnvironment()
    planner = AStarPlanner(env)
    path = planner.plan((0,0), (19,19))
    assert path is not None
    assert path[0] == (0,0)
    assert path[-1] == (19,19)
    print("test_path passed")

if __name__ == "__main__":
    test_path()
