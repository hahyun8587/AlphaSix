import numpy as np
from ..tools.AlphaZero.alphazero.environment import Environment
from ..tools.CONNSIX.connsix import draw_and_read, lets_connect
from utils import a_to_locs, locs_to_a, move_to_coords

class AlphaSixEnvironment(Environment):
    #class variables
    WHITE = -1
    BLACK = 1
    RED = 2
    
    #instance variables
    _board_size: int
    
    def __init__(self, board_size: int):
        self._board_size = board_size
    
    
    def gen_init_s(self, ip: str, port: int, color: str) -> np.ndarray:
        s = np.zeros((2, self._board_size, self._board_size), dtype=np.int32)
        
        coords = move_to_coords(lets_connect(ip, port, color).split(':'))
        
        for coord in coords:
            s[0][coord[0]][coord[1]] = self.RED 

        s[0][9][9] = self.BLACK
        s[1].fill(self.WHITE)
        
        return s
    
    
    def response(self, a: int) -> int:
        if a == -2:
            sig = draw_and_read('')
        else:
            moves = []    
            locs = a_to_locs(a)
        
            for loc in locs:
                move = ''
            
                if loc % self._board_size <= 7:
                    move = move + chr(loc % self._board_size + 65)
                else:
                    move = move + chr(loc % self._board_size + 66)
                
                move = move + str(loc // self._board_size + 19) 
                
                moves.append(move)
        
            sig = draw_and_read(':'.join(moves)) 
        
        if sig == 'WIN' or sig == 'LOSE' or 'EVEN':
            return -2 
        
        locs = []
        
        for coord in move_to_coords(sig):
            locs.append(coord[0] * self._board_size + coord[1])                    
            
        return locs_to_a(locs)
    