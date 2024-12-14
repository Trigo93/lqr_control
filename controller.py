import numpy as np
import control
from scipy.signal import cont2discrete
from config import SimConfig

class CarController:
    """! The core car control system class."""
    
    def __init__(self):
        """! Initialize the car controller with system matrices and control parameters."""
        # Discrete time conversion
        self.Ad, self.Bd, self.Cd, self.Dd, _ = cont2discrete(
            (SimConfig.A, SimConfig.B, SimConfig.C, SimConfig.D), SimConfig.DT)

        # Compute optimal feedback gain
        self.K, _, _ = control.lqr(SimConfig.A, SimConfig.B, SimConfig.Q, SimConfig.R)

    def step(self, state, command):
        """! Compute the next state given current state and control input."""
        return self.Ad @ state + self.Bd @ command

    def compute_control(self, state, ref):
        """! Compute control action using LQR feedback."""
        target = np.array([ref[0], 0, ref[2], 0])
        e = state - target
        command = -self.K.dot(e)
        return self.step(state, command)