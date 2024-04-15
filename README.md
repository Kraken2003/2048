# **Title: Reinforcement Learning for 2048 Game**

# Introduction
This repository contains implementations of reinforcement learning algorithms for training agents to play the popular 2048 game. The goal is to develop intelligent agents that can learn effective strategies for maximizing the game score by combining tiles to reach the elusive 2048 tile.

# Requirements
To run the code in this repository, you'll need:

- Python 3.x
- PyTorch
- Matplotlib
- NumPy

Ensure you have the necessary dependencies installed before running the scripts. You can install them using pip:

```bash
pip install torch matplotlib numpy
```

# Repository Structure
- **GameEmulator**: Contains classes for emulating the 2048 game environment.
- **Learning Approaches**: Includes the code for different learning agents.

# 2048 Game Implementation
This section of the repository contains the implementation of the classic 2048 game using both Pygame and NumPy array. The game is represented by a Game2048 class, which provides functionalities for playing the game, taking turns, and checking for game over conditions.

- **Pygame Implementation:**<br>
In the Pygame implementation, the game is rendered using the Pygame library to create a visual interface. The Game2048 class initializes the game window, handles user input for movements (UP, DOWN, LEFT, RIGHT), updates the game board accordingly, and displays the current score. The game loop continues until the player quits or the game is over. Additionally, there is an option to run the game with automated action inputs, making it suitable for testing and training reinforcement learning algorithms.

- **NumPy Array Implementation:**<br>
The NumPy array implementation provides a more optimized version of the game for reinforcement learning algorithms. The Game2048 class manages the game logic using NumPy arrays for efficient manipulation of the game board. It includes methods for moving the board in different directions, checking for valid moves, and updating the game state. This version is suitable for integration with reinforcement learning agents for training purposes.

# Reinforcement Learning with Monte Carlo Tree Search (MCTS)
In this section of the repository, we implement the Monte Carlo Tree Search (MCTS) algorithm for training an AI agent to play the 2048 game. The MCTS algorithm is implemented within the MonteCarlo class, which takes an instance of the Game2048 class as input.

**Monte Carlo Tree Search Algorithm**<br>
The Monte Carlo Tree Search algorithm is a probabilistic search algorithm used in decision processes, particularly in games with large state spaces. The algorithm consists of four main steps: selection, expansion, simulation, and backpropagation.

- Selection: Starting from the root node, select child nodes based on a selection policy (often UCB1) until a leaf node is reached.
- Expansion: If the selected leaf node has unexplored actions, expand the node by adding child nodes corresponding to those actions.
- Simulation: Simulate a random playout or rollout from the newly expanded node until a terminal state is reached.
- Backpropagation: Update the statistics of all nodes traversed during selection and expansion based on the outcome of the simulation.
**Implementation Details** <br>
The MonteCarlo class takes parameters such as the number of searches per move, search length, search parameter, and sample count.
- The ai_move method implements the MCTS algorithm to select the best move based on simulations and search parameters.
- The ai_play method orchestrates the AI agent's gameplay using the MCTS algorithm until a terminal state (win or loss) is reached.
- The ai_plot method provides visualization of the AI agent's performance by plotting the frequency of game scores achieved over multiple runs.

# Reinforcement Learning with Random Policy
In this section, we use a simpler approach for training an AI agent to play the 2048 game. The AI agent follows a random policy, selecting actions randomly from the action space (UP, DOWN, LEFT, RIGHT) at each step.

**Random Policy Implementation** <br>
- The AI agent selects actions randomly from the action space without considering the game state.
- The agent's gameplay is determined solely by random action selection, making it a simple baseline for comparison against more sophisticated algorithms.
**Implementation Details**<br>
- The AI agent's gameplay is controlled by a loop that iterates a specified number of times.
- At each iteration, a random action is selected from the action space and applied to the game environment.
- The game state and current board configuration are printed after each action to track the agent's progress.


# Deep Q-Network (DQN) for 2048 Game
This section of the repository contains the implementation of a Deep Q-Network (DQN) for playing the 2048 game. The DQN agent learns to play the game by interacting with the environment, storing experiences in a replay buffer, and optimizing its policy network using backpropagation.

**Components:**<br>
- Neural Network Architecture: The DQN model consists of convolutional layers followed by fully connected layers. The convolutional layers extract features from the game board, while the fully connected layers learn to estimate the Q-values for each action.

- Replay Buffer: Experiences (transitions) consisting of states, actions, rewards, and next states are stored in a replay buffer. This buffer is sampled randomly during training to break correlations between consecutive experiences.

- Epsilon-Greedy Exploration: During action selection, the agent employs an epsilon-greedy strategy to balance exploration and exploitation. With probability epsilon, the agent selects a random action to explore the environment; otherwise, it selects the action with the highest Q-value.

- Backpropagation: The policy network is optimized using the backpropagation algorithm. The loss between predicted Q-values and target Q-values is minimized using the mean squared error loss function.

- Target Network: To improve stability during training, a target network with frozen parameters is used to generate target Q-values. The target network parameters are updated periodically with the parameters of the policy network.

**Evaluation:**<br>
The trained DQN agent can be evaluated by measuring its performance in playing the 2048 game. Metrics such as the average score achieved, win rate, and convergence speed can be used to assess the agent's effectiveness in learning the game dynamics.
