import random
import numpy as np

class Game2048:
    def __init__(self):
        
        self.possible_moves = 4
        self.number_of_tiles = 16

        self.board = np.zeros((self.number_of_tiles), dtype="int")
        initial_twos = random.sample(range(self.number_of_tiles), 2)

        self.board[initial_twos] = 2
        self.board = self.board.reshape((4, 4))
        self.score = 0
        self.game_over = False

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

    def move_up(self):
        rotated_board = np.rot90(self.board, -1)
        pushed_board, has_pushed = self.push_board_right(rotated_board)
        merged_board, has_merged, score = self.merge_elements(pushed_board)
        second_pushed_board, _ = self.push_board_right(merged_board)
        rotated_back_board = np.rot90(second_pushed_board)
        move_made = has_pushed or has_merged
        self.board = rotated_back_board
        return move_made, score

    def move_down(self):
        board = np.rot90(self.board)
        board, has_pushed = self.push_board_right(board)
        board, has_merged, score = self.merge_elements(board)
        board, _ = self.push_board_right(board)
        self.board = np.rot90(board, -1)
        move_made = has_pushed or has_merged
        return move_made, score

    def move_left(self):
        board = np.rot90(self.board, 2)
        board, has_pushed = self.push_board_right(board)
        board, has_merged, score = self.merge_elements(board)
        board, _ = self.push_board_right(board)
        self.board = np.rot90(board, -2)
        move_made = has_pushed or has_merged
        return move_made, score

    def move_right(self):
        board, has_pushed = self.push_board_right(self.board)
        board, has_merged, score = self.merge_elements(board)
        board, _ = self.push_board_right(board)
        self.board = board
        move_made = has_pushed or has_merged
        return move_made, score

    def fixed_move(self):
        move_order = [self.move_left, self.move_up, self.move_down, self.move_right]
        for func in move_order:
            move_made, score = func()
            if move_made:
                return True, score
        return False, 0

    def random_move(self):
        move_made = False
        move_order = [self.move_right, self.move_up, self.move_down, self.move_left]
        while not move_made and len(move_order) > 0:
            move_index = random.randint(0, len(move_order) - 1)
            move = move_order[move_index]
            move_made, score = move()
            if move_made:
                return True, score
            move_order.pop(move_index)
        return False, 0

    def add_new_tile(self):
        empty_cells = np.argwhere(self.board == 0)
        row, col = random.choice(empty_cells)
        self.board[row, col] = 2 if random.random() < 0.9 else 4  # 90% chance of 2, 10% chance of 4

    def check_for_win(self):
        return 2048 in self.board