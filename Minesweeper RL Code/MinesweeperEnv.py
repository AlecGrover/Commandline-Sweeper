import gym
from gym import spaces
import Minesweeper_RL as Ms
import numpy as np


class CustomEnv(gym.Env):
    """Custom Environment that follows gym interface"""
    metadata = {'render.modes': ['human']}

    def __init__(self, size_x=10, size_y=10, num_mines=10):
        super(CustomEnv, self).__init__()    # Define action and observation space
        # They must be gym.spaces objects    # Example when using discrete actions:
        self.x = size_x
        self.y = size_y
        self.mines = num_mines
        self.action_space = spaces.Box(np.array([0, 0]), np.array([size_x-1, size_y-1]), dtype=np.int16)
        self.observation_space = spaces.Box(np.array([0, 0]), np.array([size_x-1, size_y-1]), dtype=np.int16)
        self.game = Ms.Minesweeper(width=size_x, height=size_y, mines=num_mines)
        _, _, _, _ = self.step(np.array([0, 0]))

    def step(self, action):
        # print(action)
        # Execute one time step within the environment
        return self.game.training_play(action[0], action[1])

    def reset(self):
        # Reset the state of the environment to an initial state
        self.game = Ms.Minesweeper(width=self.x, height=self.y, mines=self.mines)
        state, _, _, _ = self.step(np.array([0, 0]))
        return state

    def render(self, mode='human', close=False):
        # Render the environment to the screen
        self.game.print_board()


test = CustomEnv()
print(test.action_space)
print(test.action_space.high)
print(test.action_space.low)
print(test.action_space.sample())
