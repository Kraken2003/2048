from GameEmulator.MCGame import Game2048
import random
import matplotlib.pyplot as plt
import numpy as np

class MonteCarlo:
    def __init__(self, game ,searches_per_move, search_length, search_param, sample_count):
        self.searches_per_move_scale = searches_per_move
        self.search_length_scale = search_length
        self.search_param = search_param
        self.num_moves = 4
        self.sample_count = sample_count
        self.game = game

    def get_search_param(self, move_number):
        self.searches_per_move = self.searches_per_move_scale * (1+(move_number // self.search_param))
        self.search_length = self.search_length_scale * (1+(move_number // self.search_param))

    def ai_move(self,game, number_of_simulations, search_length_per_move):

        possible_first_moves = [game.move_left, game.move_up, game.move_down, game.move_right]
        first_move_scores = np.zeros(self.num_moves)

        for first_move_index in range(self.num_moves):
            first_move_function =  possible_first_moves[first_move_index]
            board_copy = np.copy(game.get_environment())
            board_with_first_move, first_move_made, first_move_score = first_move_function(board_copy)

            if first_move_made:
                board_with_first_move = game.add_new_tile(board_with_first_move)
                first_move_scores[first_move_index] += first_move_score

            else:
                continue

            for _ in range(number_of_simulations):
                move_number = 1
                search_board = np.copy(board_with_first_move)
                game_valid = True

                while game_valid and move_number < search_length_per_move:
                    search_board, game_valid, score = game.random_move(search_board)

                    if game_valid:
                        search_board = game.add_new_tile(search_board)
                        first_move_scores[first_move_index] += score
                        move_number += 1

        best_move_index = np.argmax(first_move_scores)
        best_move = possible_first_moves[best_move_index]
        search_board, game_valid, score = best_move(board_copy)
        return search_board, game_valid

    def ai_play(self, game):
        move_number = 0
        valid_game = True

        while valid_game:
            move_number += 1
            self.get_search_param(move_number)
            board, valid_game = self.ai_move(game, self.searches_per_move, self.search_length)

            if valid_game:
                board = game.add_new_tile(board)

            if game.check_for_win(board):
                valid_game = False

            print(board)
            print(move_number)

        print(board)
        return np.amax(board)
    
    def ai_plot(self, game, move_func):

        tick_locations = np.arange(1, 12)
        final_scores = []

        for i in range(self.sample_count):

            print(i,"th game -> \n")
            board = game.reset_game()
            game_end_score = self.ai_play(board)
            final_scores.append(game_end_score)

        all_counts = np.zeros(11)
        unique, counts = np.unique(np.array(final_scores), return_counts=True)
        unique = np.log2(unique).astype(int)
        index = 0

        for tick in tick_locations:
            if tick in unique:
                all_counts[tick-1] = counts[index]
                index += 1

        plt.bar(tick_locations, all_counts)
        plt.xticks(tick_locations, np.power(2, tick_locations))
        plt.xlabel("Score of Game", fontsize = 24)
        plt.ylabel(f"Frequency per {self.sample_count} runs", fontsize = 24)
        plt.show()
