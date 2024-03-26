import numpy as np
from GameEmulator.RLGame import Game2048
import matplotlib.pyplot as plt
import random

class MonteCarlo2048:
    def __init__(self, game, num_moves=4, sample_count=50, spm_scale_param=10, sl_scale_param=4, search_param=200):
        self.game = game
        self.NUMBER_OF_MOVES = num_moves
        self.SAMPLE_COUNT = sample_count
        self.SPM_SCALE_PARAM = spm_scale_param
        self.SL_SCALE_PARAM = sl_scale_param
        self.SEARCH_PARAM = search_param

    def get_search_params(self, move_number):
        self.searches_per_move = self.SPM_SCALE_PARAM * (1 + (move_number // self.SEARCH_PARAM))
        self.search_length = self.SL_SCALE_PARAM * (1 + (move_number // self.SEARCH_PARAM))
        return self.searches_per_move, self.search_length

    def check_for_win(self, board):
        return 2048 in board

    def ai_move(self, game):
        possible_moves = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        move_scores = np.zeros(self.NUMBER_OF_MOVES)
        
        for i, move in enumerate(possible_moves):
            board_copy = np.copy(game.environment_state())
            game.state_action(move)
            game.take_turn()
            if not np.array_equal(board_copy, game.environment_state()):
                move_scores[i] += game.get_score()
                for _ in range(self.searches_per_move):
                    move_number = 1
                    search_board = np.copy(game.environment_state())
                    game_over = False
                    win = False
                    
                    while not game_over and not win and move_number < self.search_length:
                        random_move = random.choice(possible_moves)
                        board_copy = np.copy(search_board)
                        game.state_action(random_move)
                        game.take_turn()
                        
                        if not np.array_equal(board_copy, game.environment_state()):
                            game.new_pieces()
                            move_scores[i] += game.get_score()
                            move_number += 1
                            game_over = game.check_game_over()
                            win = self.check_for_win(game.environment_state())
                            
        best_move_index = np.argmax(move_scores)
        best_move = possible_moves[best_move_index]
        game.state_action(best_move)
        game.take_turn()
        return game.environment_state(), not game_over, win

    def ai_play(self):
        move_number = 0
        valid_game = True
        win = False
        
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
            else:
                print(self.game.environment_state())
                print(move_number)
        
        print(self.game.environment_state())
        return np.amax(self.game.environment_state())
    
    '''
    # The following functions are used to train the AI without constantly printing the board values with each step
    def ai_play(self):
        move_number = 0
        valid_game = True
        win = False
        
        while valid_game and not win:
            move_number += 1
            self.searches_per_move, self.search_length = self.get_search_params(move_number)
            self.game.board, valid_game, win = self.ai_move(self.game)
            
            if valid_game:
                self.game.new_pieces()
                
        if win:
            print("Congratulations! You have reached 2048!")
        else:
            print("Game over! No more valid moves.")
        
        print(self.game.environment_state())
        return np.amax(self.game.environment_state())

    '''

    def ai_plot(self):
        tick_locations = np.arange(1, 12)
        final_scores = []
        
        for _ in range(self.SAMPLE_COUNT):
            game = Game2048()  # Reset game for each sample
            game_over = self.ai_play()
            final_scores.append(game_over)
        
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


if __name__ == "__main__" :

    game = Game2048()
    monte_carlo = MonteCarlo2048(game, num_moves=4, sample_count=50, 
                                 spm_scale_param=10, sl_scale_param=4, search_param=200)
    
    monte_carlo.ai_play()
    monte_carlo.ai_plot()