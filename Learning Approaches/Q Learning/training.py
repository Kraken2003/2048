from utils import hot_encoding, get_processor, same_move
from backprop import *
import torch
from GameEmulator.QGame import Game2048
from itertools import count

# Get the device (CPU or GPU) for computation
device = get_processor()

# Initialize the 2048 game emulator
game = Game2048()

# Set the number of epochs for training
epochs = 500

# Loop over episodes
for epoch in range(epochs):

    print(f"Episode {epoch}")
  
    game.reset()  
    state = hot_encoding(game.board).float()

    # Flag for the same move
    duplicate = False

    # Iterate over game steps within the epoch
    for _ in count():
        
        # Select and perform an action
        action = select_action(state)
        old_score = game.score
        old_max = game.board.max()
        game.take_turn(action.item())

        # Check if the game is over
        game_over = not game.check_valid()

        # Calculate reward 
        reward = (game.score - old_score)
        reward = torch.tensor([reward], device=device)

        # Observe new state
        if not game_over:
            next_state = hot_encoding(game.board).float()

        else:
            next_state = None

        # Check for invalid moves and penalize
        if next_state != None and torch.eq(state, next_state).all():
            
            reward -= 10
        
        # Store the transition in memory if not duplicate
        if next_state == None or len(memory) == 0 or not same_move(state, next_state, memory.memory[-1]):
            memory.push(state, action, next_state, reward)

        # Move to the next state
        state = next_state

        # If the game is over, break the loop
        if game_over:
            backprop()
            break

    # Update the target network periodically
    if epoch % TARGET_UPDATE == 0:
        target_net.load_state_dict(policy_net.state_dict())
        policy_net.train()
