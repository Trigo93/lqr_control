import pygame
import sys
import math
import numpy as np
import matplotlib.pyplot as plt
from config import SimConfig

class CarVisualizer:
    """! The visualization class for the car simulator."""
    
    def __init__(self):
        """! Initialize the visualization system."""
        pygame.init()
        self.screen = pygame.display.set_mode((SimConfig.WINDOW_LENGTH, SimConfig.WINDOW_LENGTH))
        pygame.display.set_caption("Car Simulator")

    def world_to_screen(self, x, y):
        """! Convert world coordinates to screen coordinates."""
        screen_x = int(SimConfig.WINDOW_LENGTH/2 + x * SimConfig.SCALE)
        screen_y = int(SimConfig.WINDOW_LENGTH/2 - y * SimConfig.SCALE)
        return (screen_x, screen_y)

    def draw_car(self, pos_x, pos_y, vel_x, vel_y):
        """! Draw a cute car at the specified position."""
        screen_x, screen_y = self.world_to_screen(pos_x, pos_y)
        angle = math.atan2(vel_y, vel_x)
        
        # Car body vertices
        vertices = [
            (-SimConfig.CAR_WIDTH/2, -SimConfig.CAR_HEIGHT/2),
            (SimConfig.CAR_WIDTH/2, -SimConfig.CAR_HEIGHT/2),
            (SimConfig.CAR_WIDTH/2, SimConfig.CAR_HEIGHT/2),
            (-SimConfig.CAR_WIDTH/2, SimConfig.CAR_HEIGHT/2)
        ]
        
        # Rotate and translate vertices
        rotated_vertices = []
        for x, y in vertices:
            rot_x = x * math.cos(angle) + y * math.sin(angle)
            rot_y = -x * math.sin(angle) + y * math.cos(angle)
            screen_vertex = (int(screen_x + rot_x), int(screen_y + rot_y))
            rotated_vertices.append(screen_vertex)
        
        # Draw car body
        pygame.draw.polygon(self.screen, SimConfig.RED, rotated_vertices)
        
        # Draw wheels
        wheel_positions = [
            (-SimConfig.CAR_WIDTH/3, -SimConfig.CAR_HEIGHT/2 - SimConfig.WHEEL_RADIUS/2),
            (SimConfig.CAR_WIDTH/3, -SimConfig.CAR_HEIGHT/2 - SimConfig.WHEEL_RADIUS/2),
            (-SimConfig.CAR_WIDTH/3, SimConfig.CAR_HEIGHT/2 + SimConfig.WHEEL_RADIUS/2),
            (SimConfig.CAR_WIDTH/3, SimConfig.CAR_HEIGHT/2 + SimConfig.WHEEL_RADIUS/2)
        ]
        
        for wx, wy in wheel_positions:
            rot_x = wx * math.cos(angle) + wy * math.sin(angle)
            rot_y = -wx * math.sin(angle) + wy * math.cos(angle)
            wheel_pos = (int(screen_x + rot_x), int(screen_y + rot_y))
            pygame.draw.circle(self.screen, SimConfig.DARK_GREY, wheel_pos, SimConfig.WHEEL_RADIUS)
            pygame.draw.circle(self.screen, SimConfig.LIGHT_GREY, wheel_pos, SimConfig.WHEEL_RADIUS/2)
        
        # Draw windshield
        windshield_points = [
            (SimConfig.CAR_WIDTH/4, 0),
            (SimConfig.CAR_WIDTH/2, -SimConfig.CAR_HEIGHT/3),
            (SimConfig.CAR_WIDTH/2, SimConfig.CAR_HEIGHT/3)
        ]
        
        rotated_windshield = []
        for x, y in windshield_points:
            rot_x = x * math.cos(angle) + y * math.sin(angle)
            rot_y = -x * math.sin(angle) + y * math.cos(angle)
            screen_vertex = (int(screen_x + rot_x), int(screen_y + rot_y))
            rotated_windshield.append(screen_vertex)
        
        pygame.draw.polygon(self.screen, SimConfig.BLUE, rotated_windshield)

    def draw_frame(self, state, target):
        """! Draw a complete frame of the simulation."""
        # Clear screen
        self.screen.fill(SimConfig.WHITE)

        # Draw coordinate grid
        for i in range(-10, 11):
            start_x, start_y = self.world_to_screen(i, -10)
            end_x, end_y = self.world_to_screen(i, 10)
            pygame.draw.line(self.screen, SimConfig.GRID_COLOR,
                           (start_x, start_y), (end_x, end_y))
            start_x, start_y = self.world_to_screen(-10, i)
            end_x, end_y = self.world_to_screen(10, i)
            pygame.draw.line(self.screen, SimConfig.GRID_COLOR,
                           (start_x, start_y), (end_x, end_y))

        # Draw target
        target_x, target_y = self.world_to_screen(target[0], target[2])
        pygame.draw.circle(self.screen, SimConfig.GREEN,
                         (target_x, target_y), 10)

        # Draw car
        self.draw_car(state[0], state[2], state[1], state[3])
        
        pygame.display.flip()

    def plot_trajectories(self, T, state_plot, target):
        """! Plot state trajectories after simulation."""
        fig, axs = plt.subplots(4, 1, figsize=(10, 12))
        labels = ["x", "vx", "y", "vy"]
        
        for i, ax in enumerate(axs):
            ax.plot(T, np.array(state_plot).transpose()[i], label='Actual')
            ax.plot(T, [target[i]] * len(T), "--", label='Target')
            ax.set_ylabel(labels[i])
            ax.legend()

        fig.suptitle('Car State Trajectories', fontsize=14)
        plt.show()

    def handle_events(self):
        """! Handle pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()