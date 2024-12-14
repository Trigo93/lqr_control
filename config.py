import numpy as np

class SimConfig:
    # Time and physics
    DT = 0.01  # Time step
    
    # State space matrices
    A = np.array([
        [0, 1, 0, 0],  # x  -> vx
        [0, 0, 0, 0],  # vx -> ax
        [0, 0, 0, 1],  # y  -> vy
        [0, 0, 0, 0]   # vy -> ay
    ])

    B = np.array([
        [0, 0],        # x
        [1, 0],       # vx
        [0, 0],       # y
        [0, 1]        # vy
    ])

    C = np.eye(4)
    D = np.zeros((4, 2))

    # LQR control parameters
    Q = np.diag([1, 1, 1, 1])  # State error weights
    R = np.diag([1, 1])        # Control effort weights

    # Visualization settings
    WINDOW_LENGTH = 800
    SCALE = 50  # Pixels per meter
    CAR_WIDTH = 40
    CAR_HEIGHT = 20
    WHEEL_RADIUS = 5
    
    # Colors
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    DARK_GREY = (40, 40, 40)
    LIGHT_GREY = (200, 200, 200)
    BLUE = (100, 200, 255)
    GRID_COLOR = (200, 200, 200)