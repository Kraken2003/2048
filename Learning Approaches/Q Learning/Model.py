import random
import torch
import torch.nn as nn
import torch.nn.functional as F
from collections import deque
from utils import transition, get_processor

device = get_processor()  # Initialize device to store data
Transition = transition()  # Define a transition object, used for storing experiences in ReplayBuffer

class ReplayBuffer(object):
    def __init__(self, max_size):
        """
        Initialize the replay buffer with a given maximum size.
        The buffer stores past experiences (states, actions, rewards, next_states, and dones) in a deque.
        """
        self.memory = deque([], maxlen=max_size)

    def push(self, *args):
        """
        Add a new experience to the replay buffer.
        """
        self.memory.append(Transition(*args))

    def sample(self, batch_size):
        """
        Randomly sample a batch of experiences from the replay buffer.
        """
        return random.sample(self.memory, batch_size)

    def __len__(self):
        """
        Return the number of experiences currently in the replay buffer.
        """
        return len(self.memory)
    

class ConvBlock(nn.Module):
    def __init__(self, input_dim, output_dim):
        """
        Initialize a convolutional block with 4 convolutions having different kernel sizes.
        The input dimensions are transformed to the specified number of output channels.
        """

        super(ConvBlock, self).__init__()
        d = output_dim // 4
        self.conv1 = nn.Conv2d(input_dim, d, 1, padding='same')
        self.conv2 = nn.Conv2d(input_dim, d, 2, padding='same')
        self.conv3 = nn.Conv2d(input_dim, d, 3, padding='same')
        self.conv4 = nn.Conv2d(input_dim, d, 4, padding='same')

    def forward(self, x):
        """
        Perform the forward pass through the convolutional block, applying the four convolutions to the input.
        """

        x = x.to(device)
        output1 = self.conv1(x)
        output2 = self.conv2(x)
        output3 = self.conv3(x)
        output4 = self.conv4(x)
        return torch.cat((output1, output2, output3, output4), dim=1)

class DQN(nn.Module):
    def __init__(self):
        """
        Initialize a Deep Q-Network.
        The network consists of several convolutional blocks and fully-connected layers.
        """

        super(DQN, self).__init__()
        self.conv1 = ConvBlock(16, 2048)
        self.conv2 = ConvBlock(2048, 2048)
        self.conv3 = ConvBlock(2048, 2048)
        self.dense1 = nn.Linear(2048 * 16, 1024)
        self.dense6 = nn.Linear(1024, 4)

    def forward(self, x):
        """
        Perform the forward pass through the DQN, proceeding through the convolutional and fully-connected layers.
        """

        x = x.to(device)
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = F.relu(self.conv3(x))
        x = nn.Flatten()(x)
        x = F.dropout(self.dense1(x))
        return self.dense6(x)