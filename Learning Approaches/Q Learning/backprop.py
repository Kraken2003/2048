import random
import torch
import torch.nn as nn
import torch.optim as optim
from Model import DQN, ReplayBuffer
from utils import get_processor, transition
from init_param import *

# Initialize the Transition class
Transition = transition
# Initialize the device to be used for processing
device = get_processor

# Initialize the policy network and target network
policy_net = DQN().to(device)
target_net = DQN().to(device)
target_net.eval()  # Set the target network in evaluation mode
policy_net.train()  # Set the policy network in training mode

# Initialize the optimizer
optimizer = optim.Adam(policy_net.parameters(), lr=5e-5)

# Initialize the replay buffer
memory = ReplayBuffer(50000)

# Initialize the number of steps done
steps_done = 0

def select_action(state):
    # This function selects an action based on the current state
    global steps_done
    
    sample = random.random()
    # Calculate the epsilon value
    eps_threshold = max(EPS_END, EPS_START * (EPS_DECAY ** steps_done))
    steps_done += 1
    
    if sample > eps_threshold:
        # If the sampled value is greater than the epsilon threshold, select the action with the highest Q-value
        with torch.no_grad():
            return policy_net(state).max(1)[1].view(1, 1)
        
    else:
        # If the sampled value is less than the epsilon threshold, select a random action
        return torch.tensor([[random.randrange(n_actions)]], device=device, dtype=torch.long)

def backprop():
    # This function optimizes the policy network by minimizing the loss

    if len(memory) < BATCH_SIZE:
        # If the number of transitions in the replay buffer is less than the batch size, return without doing anything
        return

    # Sample transitions from the replay buffer
    transitions = memory.sample(BATCH_SIZE)
    batch = Transition(*zip(*transitions))

    # Create a mask for the non-final next states
    non_final_mask = torch.tensor(tuple(map(lambda s: s is not None, 
                                            batch.next_state)), 
                                            device=device, dtype=torch.bool)
    
    # Extract the non-final next states
    non_final_next_states = torch.cat([s for s in batch.next_state 
                                       if s is not None])

    # Extract the state, action, and reward from the batch
    state_batch = torch.cat(batch.state)
    action_batch = torch.cat(batch.action)
    reward_batch = torch.cat(batch.reward)

    # Calculate the state-action values for the current state
    state_action_values = policy_net(state_batch).gather(1, action_batch)

    # Calculate the expected state-action values for the next state
    next_state_values = torch.zeros(BATCH_SIZE, device=device)
    next_state_values[non_final_mask] = target_net(non_final_next_states).max(1)[0].detach()

    # Calculate the actual expected state-action values
    expected_state_action_values = (next_state_values * GAMMA) + reward_batch

    # Calculate the loss
    criterion = nn.MSELoss()
    loss = criterion(state_action_values, expected_state_action_values.unsqueeze(1))

    # Zero the gradients
    optimizer.zero_grad()

    # Backpropagate the gradients
    loss.backward()

    # Update the weights
    optimizer.step()