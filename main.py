import numpy as np
from controller import CarController
from visu import CarVisualizer
from config import SimConfig
import pygame
from random import uniform

def main():
    """! Main function to run the car simulator."""
    controller = CarController()
    visualizer = CarVisualizer()

    # Define initial state and target
    initial_state = np.array([uniform(-0.5, 0.5), 0, uniform(-0.5, 0.5), 0]) * SimConfig.WINDOW_LENGTH / SimConfig.SCALE
    target = np.array([uniform(-0.5, 0.5), 0, uniform(-0.5, 0.5), 0]) * SimConfig.WINDOW_LENGTH / SimConfig.SCALE

    print("Initial state:", initial_state)
    print("Target:", target)

    # Simulation parameters
    simulation_time = 5.0
    T = np.arange(0, simulation_time, SimConfig.DT)
    
    # Run simulation
    state = initial_state
    state_plot = []
    
    for t in T:
        visualizer.handle_events()
        
        # Update state
        state_plot.append(state)
        state = controller.compute_control(state, target)
        
        # Visualize
        visualizer.draw_frame(state, target)
        pygame.time.wait(int(SimConfig.DT * 1000))
    
    # Plot final trajectories
    visualizer.plot_trajectories(T, state_plot, target)

if __name__ == "__main__":
    main()