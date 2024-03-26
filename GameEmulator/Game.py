#Creating a visual render of the 2048 game

import random  
import pygame  

class Game2048:
    """
    A class representing a game of 2048.
    """
    def __init__(self):
        """
        Initializing the Game using Pygame
        """
        pygame.init()  

        self.WIDTH = 400  # Width of the game window
        self.HEIGHT = 500  # Height of the game window
        self.screen = pygame.display.set_mode([self.WIDTH, self.HEIGHT])  # Creating game window
        pygame.display.set_caption('2048')  # Setting window title
        self.timer = pygame.time.Clock()  # Timer for controlling FPS
        self.fps = 60  # Frames per second
        self.font = pygame.font.Font('freesansbold.ttf', 24)  # Font for text rendering
        self.action_space = ['UP', 'DOWN', 'LEFT', 'RIGHT']  # Possible actions in the game
        self.observation_space = (4, 4)  # Size of the game board

        self.colors = {  # Color codes for different values and text
            0: (204, 192, 179),
            2: (238, 228, 218),
            4: (237, 224, 200),
            8: (242, 177, 121),
            16: (245, 149, 99),
            32: (246, 124, 95),
            64: (246, 94, 59),
            128: (237, 207, 114),
            256: (237, 204, 97),
            512: (237, 200, 80),
            1024: (237, 197, 63),
            2048: (237, 194, 46),
            'light text': (249, 246, 242),
            'dark text': (119, 110, 101),
            'other': (0, 0, 0),
            'bg': (187, 173, 160)
        }

        
        self.board_values = [[0 for _ in range(4)] for _ in range(4)]  # Initialize game board
        self.game_over = False  # Flag to check if game is over
        self.spawn_new = True  # Flag to check if new tile needs to be spawned
        self.init_count = 0  # Count of initial tiles
        self.direction = ''  # Direction of movement
        self.score = 0  # Game score
    
    
    def draw_over(self):
        """
        Method to draw game over screen
        """
        pygame.draw.rect(self.screen, 'black', [50, 50, 300, 100], 0, 10)  # Drawing a rectangle for game over text
        game_over_text1 = self.font.render('Game Over!', True, 'white')  # Rendering game over text
        game_over_text2 = self.font.render('Press Enter to Restart', True, 'white')  # Rendering restart instruction
        self.screen.blit(game_over_text1, (130, 65))  # Displaying game over text
        self.screen.blit(game_over_text2, (70, 105))  # Displaying restart instruction
    
    
    def draw_board(self):
        """
        Method to draw game board
        """
        pygame.draw.rect(self.screen, self.colors['bg'], [0, 0, 400, 400], 0, 10)  # Drawing game board background
        score_text = self.font.render(f'Score: {self.score}', True, 'black')  # Rendering score text
        self.screen.blit(score_text, (10, 410))  # Displaying score text
    
    
    def state_action(self, action):
        """
        
        Method to perform action in the game
        """
        self.direction = action  # Set direction based on action
        self.take_turn()  # Process the turn
        self.direction = ''  # Reset direction
        self.spawn_new = True  # Set flag to spawn new tile

    def take_turn(self):
        """
        Executes a turn based on the current direction of movement.
        """
        # Initialize a matrix to track merged tiles
        merged = [[False for _ in range(4)] for _ in range(4)]
        # Create a copy of the board to avoid modifying the original
        new_board = [row[:] for row in self.board_values]

        # Movement and merging logic for each direction
        if self.direction == 'UP':
            # Iterate over each cell in the grid
            for i in range(1, 4):
                for j in range(4):
                    # If the current cell is not empty
                    if new_board[i][j] != 0:
                        row = i
                        # Move the tile upwards as far as possible
                        while row > 0 and new_board[row - 1][j] == 0:
                            new_board[row - 1][j] = new_board[row][j]
                            new_board[row][j] = 0
                            row -= 1
                        # Merge tiles if possible and update score
                        if row > 0 and new_board[row - 1][j] == new_board[row][j] and not merged[row - 1][j]:
                            new_board[row - 1][j] *= 2
                            self.score += new_board[row - 1][j]
                            new_board[row][j] = 0
                            merged[row - 1][j] = True

        elif self.direction == 'DOWN':
            for i in range(2, -1, -1):
                for j in range(4):
                    if new_board[i][j] != 0:
                        row = i
                        while row < 3 and new_board[row + 1][j] == 0:
                            new_board[row + 1][j] = new_board[row][j]
                            new_board[row][j] = 0
                            row += 1
                        if row < 3 and new_board[row + 1][j] == new_board[row][j] and not merged[row + 1][j]:
                            new_board[row + 1][j] *= 2
                            self.score += new_board[row + 1][j]
                            new_board[row][j] = 0
                            merged[row + 1][j] = True


        elif self.direction == 'LEFT':
            for j in range(1, 4):
                for i in range(4):
                    if new_board[i][j] != 0:
                        col = j
                        while col > 0 and new_board[i][col - 1] == 0:
                            new_board[i][col - 1] = new_board[i][col]
                            new_board[i][col] = 0
                            col -= 1
                        if col > 0 and new_board[i][col - 1] == new_board[i][col] and not merged[i][col - 1]:
                            new_board[i][col - 1] *= 2
                            self.score += new_board[i][col - 1]
                            new_board[i][col] = 0
                            merged[i][col - 1] = True


        elif self.direction == 'RIGHT':
            for j in range(2, -1, -1):
                for i in range(4):
                    if new_board[i][j] != 0:
                        col = j
                        while col < 3 and new_board[i][col + 1] == 0:
                            new_board[i][col + 1] = new_board[i][col]
                            new_board[i][col] = 0
                            col += 1
                        if col < 3 and new_board[i][col + 1] == new_board[i][col] and not merged[i][col + 1]:
                            new_board[i][col + 1] *= 2
                            self.score += new_board[i][col + 1]
                            new_board[i][col] = 0
                            merged[i][col + 1] = True


        # Update the board_values
        self.board_values = new_board

    
    def environment_state(self):
        """
        Method to return current state of the environment
        """
        return self.board_values  # Return the current state of the environment (board values)
    
    
    def get_score(self):
        """
        Method to return current score
        """
        return self.score  # Return the current score


    def draw_pieces(self):
        """
        Draws each tile on the board with appropriate value and color.
        Renders value text on each tile.
        """
        # Iterate over each cell in the game board
        for i in range(4):
            for j in range(4):
                value = self.board_values[i][j]  # Get the value of the current cell
                if value > 8:
                    value_color = self.colors['light text']
                else:
                    value_color = self.colors['dark text']
                if value <= 2048:
                    color = self.colors[value]  # Get the color for the current value
                else:
                    color = self.colors['other']
                # Draw a rectangle representing the tile with appropriate color
                pygame.draw.rect(self.screen, color, [j * 95 + 20, i * 95 + 20, 75, 75], 0, 5)
                if value > 0:
                    # Render value text on the tile
                    value_len = len(str(value))
                    font = pygame.font.Font('freesansbold.ttf', 48 - (5 * value_len))
                    value_text = font.render(str(value), True, value_color)
                    text_rect = value_text.get_rect(center=(j * 95 + 57, i * 95 + 57))
                    self.screen.blit(value_text, text_rect)
                    pygame.draw.rect(self.screen, 'black', [j * 95 + 20, i * 95 + 20, 75, 75], 2, 5)

    def new_pieces(self):
        """
        Spawns new tiles on empty cells of the board.
        Returns True if the board is full, else False.
        """
        count = 0  # Counter for new tiles spawned
        full = False  # Flag to indicate if the board is full
        # Iterate over each cell in the board and spawn a new tile if the cell is empty
        while any(0 in row for row in self.board_values) and count < 1:
            row = random.randint(0, 3)  # Randomly select a row
            col = random.randint(0, 3)  # Randomly select a column
            if self.board_values[row][col] == 0:  # Check if the selected cell is empty
                count += 1
                # Randomly choose whether to spawn a tile with value 2 or 4
                if random.randint(1, 10) == 10:
                    self.board_values[row][col] = 4
                else:
                    self.board_values[row][col] = 2
        if count < 1:  # Check if no new tiles could be spawned
            full = True  # Set the flag to indicate that the board is full
        return full

    def reset_game(self):
        """
        Resets the game by initializing game variables to start a new game.
        """
        self.board_values = [[0 for _ in range(4)] for _ in range(4)]  # Reset the game board
        self.spawn_new = True  # Set flag to spawn new tile
        self.init_count = 0  # Reset initial tiles count
        self.score = 0  # Reset game score
        self.direction = ''  # Reset direction
        self.game_over = False  # Reset game over flag

    def run_game(self):
        """
        Runs the game loop.
        Handles events such as key presses.
        Draws game elements on the screen.
        Checks for game over condition and restarts the game if needed.
        Quits pygame when the game window is closed.
        """
        run = True  # Flag to control the game loop
        while run:
            self.timer.tick(self.fps)  # Limit frame rate
            self.screen.fill('gray')  # Fill the screen with gray color
            
            # Draw game elements
            self.draw_board()
            self.draw_pieces()

            # Spawn new tile if required
            if self.spawn_new or self.init_count < 2:
                self.game_over = self.new_pieces()
                self.spawn_new = False
                self.init_count += 1

            # Draw game over screen if game is over
            if self.game_over:
                self.draw_over()

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False  # Quit the game if the window is closed
                elif event.type == pygame.KEYUP:
                    # Perform action based on key press
                    if event.key == pygame.K_UP:
                        self.state_action('UP')
                    elif event.key == pygame.K_DOWN:
                        self.state_action('DOWN')
                    elif event.key == pygame.K_LEFT:
                        self.state_action('LEFT')
                    elif event.key == pygame.K_RIGHT:
                        self.state_action('RIGHT')
                    # Restart the game if it's over and Enter key is pressed
                    if self.game_over and event.key == pygame.K_RETURN:
                        self.reset_game()

            pygame.display.flip()  # Update the display
        pygame.quit()  # Quit pygame when the game loop exits


    def param_run_game(self, action):
        """
        Runs the game loop with the provided action.
        Draws game elements on the screen.
        Checks for game over condition and restarts the game if needed.
        Returns the score and board values after each move.
        """
        # Limit frame rate
        self.timer.tick(self.fps)
        # Fill the screen with gray color
        self.screen.fill('gray')
        
        # Draw game elements
        self.draw_board()
        self.draw_pieces()

        # Spawn new tile if required
        if self.spawn_new or self.init_count < 2:
            self.game_over = self.new_pieces()
            self.spawn_new = False
            self.init_count += 1

        # Draw game over screen if game is over
        if self.game_over:
            self.draw_over()

        # Apply the provided action
        self.state_action(action)

        # Update the display
        pygame.display.flip()

        # Check if the game is over
        if self.game_over:
            self.reset_game()  # Restart the game if it's over

        # Return the score and board values after each move
        return self.get_score(), self.board_values
    
    def rl_run_game(self, action):
        """
        Runs the game loop with the provided action.
        Checks for game over condition and restarts the game if needed.
        Returns the score and board values after each move.
        """
        # Apply the provided action
        self.state_action(action)

        # Spawn new tile if required
        if self.spawn_new or self.init_count < 2:
            self.game_over = self.new_pieces()
            self.spawn_new = False
            self.init_count += 1

        # Check if the game is over
        if self.game_over:
            self.reset_game()  # Restart the game if it's over

        # Return the score and board values after each move
        return self.get_score(), self.board_values

#Running the 2048 Game
if __name__ == "__main__":
    game = Game2048()
    game.run_game()
