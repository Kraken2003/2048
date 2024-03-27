import random
import numpy as np

class Game2048:
    def __init__(self):
        
        self.possible_moves = 4
        self.number_of_tiles = 16

    def reset_game(self):
        self.board = np.zeros((self.number_of_tiles), dtype="int")
        initial_twos = random.sample(range(self.number_of_tiles), 2)

        self.board[initial_twos] = 2
        self.board = self.board.reshape((4, 4))

    def get_environment(self):
        return self.board
    
    def add_new_tile(self, board):
        empty_cells = np.argwhere(board == 0)
        row, col = random.choice(empty_cells)
        board[row, col] = 2 if random.random() < 0.9 else 4  # 90% chance of 2, 10% chance of 4
        return board

    def check_for_win(self, board):
        return 2048 in board

    def push_board_right(self, board):
        new = np.zeros((4, 4), dtype="int")
        done = False
        for row in range(4):
            count = 3
            for col in range(3, -1, -1):
                if board[row][col] != 0:
                    new[row][count] = board[row][col]
                    if col != count:
                        done = True
                    count -= 1
        return new, done

    def merge_elements(self, board):
        score = 0
        done = False
        for row in range(4):
            for col in range(3, 0, -1):
                if board[row][col] == board[row][col - 1] and board[row][col] != 0:
                    board[row][col] *= 2
                    score += board[row][col]
                    board[row][col - 1] = 0
                    done = True
        return board, done, score

    def move_up(self, board):
        rotated_board = np.rot90(board, -1)
        pushed_board, has_pushed = self.push_board_right(rotated_board)
        merged_board, has_merged, score = self.merge_elements(pushed_board)
        second_pushed_board, _ = self.push_board_right(merged_board)
        rotated_back_board = np.rot90(second_pushed_board)
        move_made = has_pushed or has_merged
        board = rotated_back_board
        return board, move_made, score

    def move_down(self, board):
        board = np.rot90(board)
        board, has_pushed = self.push_board_right(board)
        board, has_merged, score = self.merge_elements(board)
        board, _ = self.push_board_right(board)
        board = np.rot90(board, -1)
        move_made = has_pushed or has_merged
        return board, move_made, score

    def move_left(self, board):
        board = np.rot90(board, 2)
        board, has_pushed = self.push_board_right(board)
        board, has_merged, score = self.merge_elements(board)
        board, _ = self.push_board_right(board)
        board = np.rot90(board, -2)
        move_made = has_pushed or has_merged
        return board, move_made, score

    def move_right(self, board):
        board, has_pushed = self.push_board_right(board)
        board, has_merged, score = self.merge_elements(board)
        board, _ = self.push_board_right(board)
        board = board
        move_made = has_pushed or has_merged
        return board ,move_made, score

    def random_move(self, board):
        move_made = False
        possible_moves = [self.move_right, self.move_up, self.move_down, self.move_left]
        while not move_made and len(possible_moves) > 0:
            move_index = random.randint(0, len(possible_moves) - 1)
            move = possible_moves[move_index]
            move_made, score = move(board)
            if move_made:
                return board, True, score
            possible_moves.pop(move_index)
        return board, False, 0