# src/visualizer.py
import pygame
import sys
from simulation.config import GRID_SIZE, CELL_SIZE, FPS

class Visualizer:
    def __init__(self, environment, robot_navigator):
        pygame.init()
        self.env = environment
        self.robot = robot_navigator
        self.width = GRID_SIZE * CELL_SIZE
        self.height = GRID_SIZE * CELL_SIZE
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Autonomous Navigation - Water Quality")
        self.clock = pygame.time.Clock()
    
    def draw_grid(self):
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                rect = pygame.Rect(y*CELL_SIZE, x*CELL_SIZE, CELL_SIZE, CELL_SIZE)
                if self.env.is_obstacle(x, y):
                    color = (80,80,80)
                else:
                    water = self.env.get_water_quality(x, y)
                    if water:
                        chl = water.get('chlorophyll_a_ugL', 0)
                        red = min(255, int(255 * chl / 50))
                        green = 255 - red
                        color = (red, green, 0)
                    else:
                        color = (200,200,200)
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, (0,0,0), rect, 1)
        rx, ry = self.robot.x, self.robot.y
        center = (ry*CELL_SIZE + CELL_SIZE//2, rx*CELL_SIZE + CELL_SIZE//2)
        pygame.draw.circle(self.screen, (0,0,255), center, CELL_SIZE//3)
    
    def run(self, path):
        if not path:
            return
        path_index = 0
        running = True
        while running and path_index < len(path):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            target = path[path_index]
            if (self.robot.x, self.robot.y) == target:
                path_index += 1
            else:
                self.robot.move(*target)
            self.screen.fill((0,0,0))
            self.draw_grid()
            self.clock.tick(FPS)
            pygame.display.flip()
        pygame.quit()
        sys.exit()
