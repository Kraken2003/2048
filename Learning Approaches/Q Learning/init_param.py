# Initialize the neural network for DQN agent
BATCH_SIZE = 64  # Mini-batch size for training
GAMMA = 0.99  # Discount factor for future rewards
EPS_START = 0.9  # Starting value of epsilon for epsilon-greedy action selection
EPS_END = 0.01  # Minimum value of epsilon for epsilon-greedy action selection
EPS_DECAY = 0.9999  # Decay factor for epsilon
TARGET_UPDATE = 20  # Number of timesteps between updates of the target network

# Define the number of possible actions
n_actions = 4