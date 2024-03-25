import glob
import os

import torch  # pytorch
import random
import numpy as np  # numpy
from collections import deque  # data structure to store memory

from snake_ai.constants import MAP_SIZE, HIDDEN_LAYER, MAX_MEMORY, LR, BATCH_SIZE, GAMMA
from snake_ai.game import SnakeGameAI  # importing the game created in step 1
from snake_ai.json_manager import read_data
from snake_ai.model import LinearQNet, QTrainer  # importing the neural net from step 2


class Agent:
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0.02  # randomness
        self.memory = deque(maxlen=MAX_MEMORY)

        self.model = LinearQNet(1, MAP_SIZE, HIDDEN_LAYER, 3)  # input size, hidden size, output size
        self.trainer = QTrainer(self.model, lr=LR, gamma=GAMMA)

        self.trained_random_nr = 0
        self.trained_nr = 0

        self.max_record = read_data().record

    def load_latest_model(self):
        model_files = glob.glob('./model/model_*.pth')
        if model_files:
            latest_model = max(model_files, key=os.path.getctime)
            self.model = LinearQNet.load(latest_model)

    @staticmethod
    def get_state(game: SnakeGameAI):
        near = game.goodMove

        state = [
            near,
            # map in one dimension
            *game.map
        ]
        return np.array(state, dtype=int)

    def remember(self, state, action, reward, next_state, done, score):
        if score > self.max_record - 3:
            self.memory.append((state, action, reward, next_state, done))  # popleft if MAX_MEMORY is reached

    def train_long_memory(self, score):
        if score > self.max_record - 3:
            if len(self.memory) > BATCH_SIZE:
                mini_sample = random.sample(self.memory, BATCH_SIZE)  # list of tuples
                self.trained_random_nr += 1
                print("trained_random_nr" + str(self.trained_random_nr))
            else:
                mini_sample = self.memory
                self.trained_nr += 1
                print("trained_nr" + str(self.trained_nr))

            states, actions, rewards, next_states, dones = zip(*mini_sample)
            self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done, score):
        if score > self.max_record - 3:
            self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        self.epsilon = 1000 - self.n_games
        final_move = [0, 0, 0]
        if random.randint(0, 2500) < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return final_move
