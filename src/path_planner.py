# src/path_planner.py
import heapq
import math

class AStarPlanner:
    def __init__(self, environment):
        self.env = environment
    
    def heuristic(self, a, b):
        return math.hypot(a[0]-b[0], a[1]-b[1])
    
    def get_neighbors(self, node):
        x, y = node
        neighbors = []
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = x+dx, y+dy
            if 0 <= nx < self.env.grid_size and 0 <= ny < self.env.grid_size:
                if not self.env.is_obstacle(nx, ny):
                    neighbors.append((nx, ny))
        return neighbors
    
    def plan(self, start, goal):
        if self.env.is_obstacle(*start) or self.env.is_obstacle(*goal):
            return None
        
        open_set = []
        heapq.heappush(open_set, (0, start))
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.heuristic(start, goal)}
        
        while open_set:
            _, current = heapq.heappop(open_set)
            if current == goal:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(start)
                path.reverse()
                return path
            for neighbor in self.get_neighbors(current):
                tentative_g = g_score[current] + 1
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score[neighbor] = tentative_g + self.heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
        return None
