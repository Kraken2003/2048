import random
import numpy as np
from numpy import zeros, rot90, array

class Game2048():
    """
    Class to represent the 2048 game.

    Attributes:
        cell_count (int): The number of cells in each row and column of the game board.
        board (numpy.ndarray): A 2D array representing the game board.
        game_over (bool): A flag indicating whether the game is over.
        score (int): The current score of the game.
    """

    def __init__(self):
        """
        Initialize the game.

        Initializes the game board with empty cells, sets the game_over flag to False,
        and initializes the score to 0.
        """
        self.cell_count = 4
        self.reset()

    def reset(self):
        """
        Reset the game.

        Resets the game board with all cells set to zero, draws new pieces on the board,
        resets the game_over flag to False, and sets the score to 0.
        """

        self.board = zeros((self.cell_count, self.cell_count), dtype=int)
        self.draw_new_pieces()
        self.game_over = False
        self.score = 0

    def draw_new_pieces(self):
        """
        Draw new pieces on the board.

        Randomly selects an empty cell on the board and places either a '2' or a '4' on that cell.
        The probability of placing a '2' is 90%, and the probability of placing a '4' is 10%.
        """

        empty_cells = np.argwhere(self.board == 0)
        if empty_cells.size != 0:
            row, col = random.choice(empty_cells)
            self.board[row, col] = 2 if random.random() < 0.9 else 4

    def move_left(self, col):
        """
        Move numbers to the left in a column.

        Combines adjacent numbers in the given column that are equal, moving them leftward,
        and updates the score accordingly.

        Args:
            col (numpy.ndarray): The column of numbers to be moved.

        Returns:
            numpy.ndarray: The updated column after moving the numbers to the left.
        """

        new_col = zeros((self.cell_count), dtype=col.dtype)
        j = 0
        previous = None
        for i in range(col.size):
            if col[i] != 0:  # number different from zero
                if previous is None:
                    previous = col[i]
                else:
                    if previous == col[i]:
                        new_col[j] = 2 * col[i]
                        self.score += new_col[j]
                        j += 1
                        previous = None
                    else:
                        new_col[j] = previous
                        j += 1
                        previous = col[i]
        if previous is not None:
            new_col[j] = previous
        return new_col

    def move(self, direction):
        """
        Move the board in a given direction.

        Moves the entire board (all rows and columns) in the specified direction by
        rotating the board, performing leftward movement on each column, and rotating
        the board back to its original orientation.

        Args:
            direction (int): The direction in which to move the board.
                             0: left, 1: up, 2: right, 3: down

        Returns:
            numpy.ndarray: The updated game board after moving in the specified direction.
        """

        rotated_board = rot90(self.board, direction)
        cols = [rotated_board[i, :] for i in range(self.cell_count)]
        new_board = array([self.move_left(col) for col in cols])
        return rot90(new_board, -direction)

    def check_valid(self):
        """
        Check if there are valid moves left.

        Checks if there are any empty cells on the board or if there are adjacent cells
        with the same value that can be merged.

        Returns:
            bool: True if there are valid moves left, False otherwise.
        """
        
        for i in range(self.cell_count):
            for j in range(self.cell_count):
                if self.board[i][j] == 0:
                    return True
                if i != 0 and self.board[i - 1][j] == self.board[i][j]:
                    return True
                if j != 0 and self.board[i][j - 1] == self.board[i][j]:
                    return True
        return False

    def take_turn(self, direction):
        """
        Take a turn by moving the board in a direction.

        Moves the board in the specified direction, updates the board and score if the move
        is valid, and draws new pieces on the board. If the move does not change the board,
        no new piece is drawn.

        Args:
            direction (int): The direction in which to move the board.
                             0: left, 1: up, 2: right, 3: down
        """
        
        new_board = self.move(direction)
        if not (new_board == self.board).all():
            self.board = new_board
            self.draw_new_pieces()