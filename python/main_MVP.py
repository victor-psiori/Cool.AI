import numpy as np
import gym

from keras.models import Sequential, Model
from keras.layers import Dense, Activation, Flatten, Input, Concatenate
from keras.optimizers import Adam

from rl.agents import DDPGAgent
from rl.memory import SequentialMemory
from rl.random import OrnsteinUhlenbeckProcess

# Import a few other funcs for the main script
import argparse, os, yaml
import sys

ENV_NAME = "AllVar-v0"

env = gym.make(ENV_NAME)

oberservation = env.reset()

# get action for the current state and go one step in environment
action = np.array([0.5, 0.5, 0.5, 0.5, 0.5])
next_state, reward, done, info = env.step(action)
Tout = next_state[0]

data = []

if __name__ == "__main__":

    config_file = "config/config.yml"
    with open(config_file, "r") as ymlfile:
        cfg = yaml.load(ymlfile)

    num_episodes = cfg["test_episodes"]  # 1
    target_temp = cfg["TOUT1_target"]  # 22
    alpha = cfg["rate_change"]  # -1.0
    scores, episodes = [], []
    Tout = []
    for e in range(num_episodes):
        done = False
        score = 0
        step = 0
        # state space => [T_out_Z1, T_out_Z2, pue]
        state = env.reset()
        while not done:
            adjust = (target_temp - next_state[0]) * alpha
            action = np.array([adjust, adjust, 0, 0, 0])
            step += 1
            next_state, reward, done, info = env.step(action)
            Tout.append(next_state[0])
			if not done or score == 499:
				reward = reward
			else:
				# whenver episode is done, reward is reset to -100.
				reward = -100
            # increment score by reward at each time step.
			score += reward
            state = next_state
            if done:
				if score == 500:
					score = score
				else:
					score = score + 100
                scores.append(score)
                episodes.append(e)
                print("episode:", e, "  score:", score, "  steps:", step)
				# terminate the episdode if mean-score of last 10 time steps
				# are > 490.
                if np.mean(scores[-min(10, len(scores)) :]) > 490:
                    sys.exit()
            # also exit the loop, if number of time-steps exceed 200.
			if step >= 200:
                sys.exit()
