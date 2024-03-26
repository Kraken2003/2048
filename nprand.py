import random
from game2048 import Game2048

# List of all possible actions
action_space = ['UP', 'DOWN', 'LEFT', 'RIGHT']

if __name__ == "__main__":
    game = Game2048()
    for _ in range(10):
        # Randomly choose an action from the action space
        action = random.choice(action_space)
        game.state_action(action)
        game.take_turn()
        if game.new_pieces():
            print("Game over! Board is full.")
            game.game_over = True
        else:
            print("Current board state:")
            print(game.board)
