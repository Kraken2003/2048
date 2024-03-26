#Using Numpy array instead of pygame to optimize the code for Reinforcement Learning Algorithms

import random
import numpy as np

class Game2048:
    def __init__(self):
        self.board = np.zeros((4, 4), dtype=int)
        self.score = 0
        self.game_over = False

    def state_action(self, action):
        # Set direction based on action
        self.direction = action

    def take_turn(self):
        merged = np.zeros((4, 4), dtype=bool)

        if self.direction == 'UP':
            for j in range(4):
                for i in range(1, 4):
                    if self.board[i][j] != 0:
                        row = i
                        while row > 0 and self.board[row - 1][j] == 0:
                            self.board[row - 1][j] = self.board[row][j]
                            self.board[row][j] = 0
                            row -= 1
                        if row > 0 and self.board[row - 1][j] == self.board[row][j] and not merged[row - 1][j]:
                            self.board[row - 1][j] *= 2
                            self.score += self.board[row - 1][j]
                            self.board[row][j] = 0
                            merged[row - 1][j] = True

        elif self.direction == 'DOWN':
            for j in range(4):
                for i in range(2, -1, -1):
                    if self.board[i][j] != 0:
                        row = i
                        while row < 3 and self.board[row + 1][j] == 0:
                            self.board[row + 1][j] = self.board[row][j]
                            self.board[row][j] = 0
                            row += 1
                        if row < 3 and self.board[row + 1][j] == self.board[row][j] and not merged[row + 1][j]:
                            self.board[row + 1][j] *= 2
                            self.score += self.board[row + 1][j]
                            self.board[row][j] = 0
                            merged[row + 1][j] = True

        elif self.direction == 'LEFT':
            for i in range(4):
                for j in range(1, 4):
                    if self.board[i][j] != 0:
                        col = j
                        while col > 0 and self.board[i][col - 1] == 0:
                            self.board[i][col - 1] = self.board[i][col]
                            self.board[i][col] = 0
                            col -= 1
                        if col > 0 and self.board[i][col - 1] == self.board[i][col] and not merged[i][col - 1]:
                            self.board[i][col - 1] *= 2
                            self.score += self.board[i][col - 1]
                            self.board[i][col] = 0
                            merged[i][col - 1] = True

        elif self.direction == 'RIGHT':
            for i in range(4):
                for j in range(2, -1, -1):
                    if self.board[i][j] != 0:
                        col = j
                        while col < 3 and self.board[i][col + 1] == 0:
                            self.board[i][col + 1] = self.board[i][col]
                            self.board[i][col] = 0
                            col += 1
                        if col < 3 and self.board[i][col + 1] == self.board[i][col] and not merged[i][col + 1]:
                            self.board[i][col + 1] *= 2
                            self.score += self.board[i][col + 1]
                            self.board[i][col] = 0
                            merged[i][col + 1] = True

        self.direction = ''  # Reset direction

    def new_pieces(self):
        empty_cells = np.argwhere(self.board == 0)
        if len(empty_cells) == 0:
            return True  # Board is full

        row, col = random.choice(empty_cells)
        self.board[row, col] = 2 if random.random() < 0.9 else 4  # 90% chance of 2, 10% chance of 4
        return False  # Board is not full

    def environment_state(self):
        return self.board.copy()

    def get_score(self):
        return self.score
    
    def check_for_win(self, board):
        return 2048 in board

    def reset_game(self):
        self.board = np.zeros((4, 4), dtype=int)
        self.score = 0
        self.game_over = False

    def run_game(self):
        while not self.game_over:
            # Get user input or select action programmatically
            action = input("Enter action: ")
            self.state_action(action)
            self.take_turn()
            if self.new_pieces():
                print("Game over! Board is full.")
                self.game_over = True
            else:
                print("Current board state:")
                print(self.board)




