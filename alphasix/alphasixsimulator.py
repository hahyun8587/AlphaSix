import numpy as np
from tools.AlphaZero.alphazero.simulator import Simulator
from alphasix.utils import atoc

class AlphaSixSimulator(Simulator):
    """Simulator of alphasix.
    
    Sets size of the board and max number of red stones of this instance.
    
    The state of alphasix is 2 x `board_size` x `board_size` 
    3D array where,
    * The first plane represents stones on the board.
    * The second plane represents turn of a player. 
    
    The first plane of initial state has `0` to `max_reds` number of red stones
    and `1` black stone on the center. The second plane is filled with 
    `AlphaSixSimulator.WHITE` to indicate turn of white.
    
    Args:
        board_size (int): The size of the board.
            It should be odd and bigger than `7`.
        max_red (int): The max number of red stones.
            It should be in the range of `[0, 5]`.
    """
    
    #class variables
    BLACK = -1
    WHITE = 1
    RED = 2
    
    #instance variables
    _board_size: int
    _max_red: int
    
    def __init__(self, board_size: int, max_red: int):
        self._board_size = board_size
        self._max_red = max_red
    
        
    def gen_init_s(self) -> np.ndarray:
        rng = np.random.default_rng()
        stones = np.zeros((self._board_size, self._board_size))
        
        for loc in rng.choice(self._board_size * self._board_size, 
                              size=rng.choice(self._max_red + 1), 
                              replace=False):
            stones[loc // self._board_size][loc % self._board_size] \
                    = AlphaSixSimulator.RED
        
        stones[self._board_size // 2][self._board_size // 2] \
                = AlphaSixSimulator.BLACK
        
        turn = np.full((self._board_size, self._board_size), 
                       AlphaSixSimulator.WHITE, dtype=float)    
                
        return np.stack((stones, turn))
  
    
    def simulate(self, s: np.ndarray, a: int) -> tuple:
        coords = atoc(a, self._board_size)
        is_invalid_a = False
        
        for coord in coords:
            if s[0][coord[0]][coord[1]] != 0:
                is_invalid_a = True
                
                break

        if is_invalid_a:
            return (-1, None)
        
        s_prime = np.array(s)
         
        for coord in coords:
            s_prime[0][coord[0]][coord[1]] = s[1][0][0]
            
        s_prime[1].fill(-s[1][0][0])
        
        return (1 if self.is_terminal(s_prime) else 0, s_prime)
        
       
    def is_terminal(self, s: np.ndarray) -> bool:
        None
                
                   