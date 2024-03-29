import math
import torch
import torch.nn.functional as F
from collections import namedtuple

def get_processor():
   """
    Returns the device that will be used for processing, either CUDA (if available)
    or CPU.
    """
   return torch.device("cuda" if torch.cuda.is_available() else "cpu")

def hot_encoding(board):
  """
    Encodes the game board using one-hot encoding. The board is flattened, and each
    non-zero element is replaced with its base-2 logarithm (rounded down). The
    resulting sequence is converted to a LongTensor and then one-hot encoded using
    the F.one_hot function from PyTorch. The encoded tensor is then reshaped and
    permuted to match the desired output format.
    """
  board_flat = [0 if e == 0 else int(math.log(e,2)) for e in board.flatten()]
  board_flat = torch.LongTensor(board_flat)
  board_flat = F.one_hot(board_flat, num_classes=16).float().flatten()
  board_flat = board_flat.reshape(1, 4, 4, 16).permute(0, 3, 1, 2)
  return board_flat

def transition():
  """
    Returns a namedtuple `Transition` with elements state, action, next_state, and reward.
    This namedtuple is used to represent a single transition in the reinforcement learning
    environment, where state represents the current state of the environment, action is
    the action taken by the agent in the current state, next_state represents the
    resulting state of the environment after the action has been taken, and reward is
    the reward obtained by the agent for taking the action in the current state.
    """
  return namedtuple('Transition',
                        ('state', 'action', 'next_state', 'reward'))

def same_move(state, next_state, last_memory):
  """
    Checks if the state and next_state are the same as the state and next_state
    contained in the last_memory object.
    """
  return torch.eq(state, last_memory.state).all() and torch.eq(next_state, last_memory.next_state).all()

