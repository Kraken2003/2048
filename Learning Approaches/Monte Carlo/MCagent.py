import numpy as np
import random
import matplotlib.pyplot as plt
from GameEmulator.RLGame import Game2048

class MonteCarlo2048:
    def __init__(self, game, num_moves=4, sample_count=50, spm_scale_param=10, sl_scale_param=4, search_param=200):
        """
        Initialize the Monte Carlo AI agent for the 2048 game.

        Parameters:
        - game: The instance of the 2048 game.
        - num_moves: Number of possible moves (default is 4 for UP, DOWN, LEFT, RIGHT).
        - sample_count: Number of samples to run for AI plotting.
        - spm_scale_param: Scaling parameter for searches per move.
        - sl_scale_param: Scaling parameter for search length.
        - search_param: Parameter for determining when to increase searches per move and search length.
        """
        self.game = game
        self.NUMBER_OF_MOVES = num_moves
        self.SAMPLE_COUNT = sample_count
        self.SPM_SCALE_PARAM = spm_scale_param
        self.SL_SCALE_PARAM = sl_scale_param
        self.SEARCH_PARAM = search_param

    def get_search_params(self, move_number):
        """
        Adjust the search parameters based on the current move number.

        Parameters:
        - move_number: The current move number.

        Returns:
        - searches_per_move: Adjusted searches per move.
        - search_length: Adjusted search length.
        """
        self.searches_per_move = self.SPM_SCALE_PARAM * (1 + (move_number // self.SEARCH_PARAM))
        self.search_length = self.SL_SCALE_PARAM * (1 + (move_number // self.SEARCH_PARAM))
        return self.searches_per_move, self.search_length

    def check_for_win(self, board):
        """
        Check if the game board contains the winning tile (2048).

        Parameters:
        - board: The game board.

        Returns:
        - True if 2048 is present, False otherwise.
        """
        return 2048 in board

    def ai_move(self, game):
        """
        Perform an AI move for the 2048 game.

        Parameters:
        - game: The instance of the 2048 game.

        Returns:
        - The updated game board, flag indicating game continuation, and flag indicating win.
        """
        possible_moves = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        move_scores = np.zeros(self.NUMBER_OF_MOVES)
        win = False

        move_made = False

        for i, move in enumerate(possible_moves):
            board_copy = np.copy(game.environment_state())
            game.state_action(move)
            game.take_turn()

            if not np.array_equal(board_copy, game.environment_state()):
                move_scores[i] += game.get_score()
                move_made = True

                for _ in range(self.searches_per_move):
                    move_number = 1
                    search_board = np.copy(game.environment_state())
                    game.game_over = False
                    win = False  # Reset win for each move
                    
                    while not game.game_over and not win and move_number < self.search_length:
                        random_move = random.choice(possible_moves)
                        board_copy = np.copy(search_board)
                        game.state_action(random_move)
                        game.take_turn()
                        move_number += 1
                        
                        if not np.array_equal(board_copy, game.environment_state()):
                            game.new_pieces()
                            move_scores[i] += game.get_score()
                            game.game_over = game.new_pieces()
                            win = self.check_for_win(game.environment_state())
               
        if not move_made:
            game.game_over = True

        best_move_index = np.argmax(move_scores)
        best_move = possible_moves[best_move_index]
        game.state_action(best_move)
        game.take_turn()
        return game.environment_state(), not game.game_over, win

    def ai_play(self):
        """
        Play the 2048 game using the AI agent.

        Returns:
        - The maximum tile value achieved during the game.
        """
        move_number = 0
        valid_game = True
        win = False
        self.game.new_pieces()
        self.game.new_pieces()

        while valid_game and not win:
            move_number += 1
            self.searches_per_move, self.search_length = self.get_search_params(move_number)
            self.game.board, valid_game, win = self.ai_move(self.game)
            
            if valid_game:
                self.game.new_pieces()
                
            if win:
                print("Congratulations! You have reached 2048!")
            elif not valid_game:
                print("Game over! No more valid moves.")

        return np.amax(self.game.environment_state())
    
    def ai_plot(self):
        """
        Plot the frequency of achieving different scores over multiple AI plays.
        """
        tick_locations = np.arange(1, 12)
        final_scores = []
        
        for i in range(self.SAMPLE_COUNT):
            if i % 20 == 0:
                print(f"sample count {i}")
            game.reset_game() # Reset game for each sample
            game_finished = self.ai_play()
            final_scores.append(game_finished)
        
        all_counts = np.zeros(11)
        unique, counts = np.unique(np.array(final_scores), return_counts=True)
        unique = np.log2(unique).astype(int)
        index = 0
        
        for tick in tick_locations:
            if tick in unique:
                all_counts[tick - 1] = counts[index]
                index += 1
        
        plt.bar(tick_locations, all_counts)
        plt.xticks(tick_locations, np.power(2, tick_locations))
        plt.xlabel("Score of Game", fontsize=24)
        plt.ylabel(f"Frequency per {self.SAMPLE_COUNT} runs", fontsize=24)
        plt.show()


# Testing code
if __name__ == "__main__" :

    game = Game2048()
    monte_carlo = MonteCarlo2048(game, num_moves=4, sample_count=50, 
                                 spm_scale_param=10, sl_scale_param=4, search_param=200)
    monte_carlo.ai_plot()