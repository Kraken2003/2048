from GameCode import Game2048
import random
import time

def play_game():
    # Create an instance of the Game2048 class
    game = Game2048()
    
    # Run the game loop
    for _ in range(10):
        # Generate a random action (UP, DOWN, LEFT, RIGHT)
        action = random.choice(game.action_space)
        
        # Run the game with the random action and get the score and board values
        score, board_values = game.param_run_game(action)
        
        # Print the current score and board values
        print(f"Score: {score}")
        print("Board Values:")
        for row in board_values:
            print(row)

        time.sleep(1)
# Run the function to play the game
play_game()