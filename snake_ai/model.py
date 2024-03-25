import datetime
import torch
import torch.nn as nn
import torch.optim as optim
import os

# Determine if CUDA is available
from snake_ai.constants import MAP_SIZE, HIDDEN_LAYER
from snake_ai.json_manager import read_data, add_data_record_model
from snake_ai.record_model import RecordModel

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")


class LinearQNet(nn.Module):
    def __init__(self, input_size_direction, input_size_map, hidden_size, output_size):
        super(LinearQNet, self).__init__()
        self.linear_direction = nn.Linear(input_size_direction, (hidden_size // 8))
        self.linear_map = nn.Linear(input_size_map, (hidden_size // 8) * 7)
        self.relu1 = nn.ReLU()
        self.linear2 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        # Ensure x has at least two dimensions (batch dimension and input features)
        if len(x.shape) == 1:
            x = x.unsqueeze(0)  # Add batch dimension if missing

        x1 = self.linear_direction(x[:, :1])
        x2 = self.linear_map(x[:, 1:])
        combine = torch.cat((x1, x2), dim=1)
        x = self.relu1(combine)
        x = self.linear2(x)

        return x

    def save(self, record, reward_all_steps_in_one_game, file_name=None):
        model_folder_path = './model'
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)

        if file_name is None:
            current_time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S-%f')
            file_name = f"model_{current_time}_record{record}.pth"

        session_record = read_data().record

        if record >= session_record:
            file_name = os.path.join(model_folder_path, file_name)
            torch.save(self.state_dict(), file_name)
            record_model = RecordModel(record=record, reward=reward_all_steps_in_one_game, model_name=file_name)
            add_data_record_model(record_model)

    @classmethod
    def load(cls, file_name='model.pth'):
        model_folder_path = ''
        file_name = os.path.join(model_folder_path, file_name)

        model = cls(1, MAP_SIZE, HIDDEN_LAYER, 3).to(device)  # Move model to the device
        model.load_state_dict(torch.load(file_name, map_location=device))  # Load the model to the appropriate device
        return model


class QTrainer:
    def __init__(self, model, lr, gamma):
        self.lr = lr
        self.gamma = gamma
        self.model = model
        self.optimizer = optim.Adam(model.parameters(), lr=self.lr)
        self.criterion = nn.MSELoss()

    def train_step(self, state, action, reward, next_state, done):
        state = torch.tensor(state, dtype=torch.float).to(device)
        next_state = torch.tensor(next_state, dtype=torch.float).to(device)
        action = torch.tensor(action, dtype=torch.long).to(device)
        reward = torch.tensor(reward, dtype=torch.float).to(device)

        if len(state.shape) == 1:
            state = torch.unsqueeze(state, 0)
            next_state = torch.unsqueeze(next_state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            done = (done,)

        pred = self.model(state)

        target = pred.clone()
        for idx in range(len(done)):
            q_new = reward[idx]
            if not done[idx]:
                calc_disc = self.gamma * torch.max(self.model(next_state[idx]))
                q_new = reward[idx] + calc_disc
            target[idx][torch.argmax(action[idx]).item()] = q_new

        self.optimizer.zero_grad()
        loss = self.criterion(target, pred)
        loss.backward()
        self.optimizer.step()
