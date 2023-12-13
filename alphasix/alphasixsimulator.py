import numpy as np
from tools.AlphaZero.alphazero.simulator import Simulator
from utils import a_to_locs

class AlphaSixSimulator(Simulator):
    """Simulator of alphasix.
    """
    
    #class variables
    WHITE = -1
    BLACK = 1
    RED = 2
    _board_size = 19
    _max_red_stones = 5
    
    @classmethod
    def gen_init_s(cls) -> np.ndarray:
        s = np.zeros((2, cls._board_size, cls._board_size), dtype=np.int32)
        n_red_stone = np.random.choice(cls._max_red_stones + 1)
        red_stone_loc = np.random.choice(cls._board_size ** 2, n_red_stone)

        for loc in red_stone_loc:
            s[0][loc // cls._board_size][loc % cls._board_size] = cls.RED
        
        s[0][9][9] = cls.BLACK
        s[1].fill(cls.WHITE)
        
        return s
    
    
    def simulate(self, s: np.ndarray, a: int) -> np.ndarray:
        next_s = s.copy()
        locs = a_to_locs(a)
        
        for i in range(2):
            if next_s[0][locs[i] // self._board_size][locs[i] % self._board_size] != 0:
                return None
        
            next_s[0][locs[i] // self._board_size][locs[i] % self._board_size] = s[1][0][0]
            
        next_s[1].fill(-s[1][0][0])
        
        return next_s
    
    
    def is_terminal(self, s: np.ndarray, a: int) -> bool:
        direction = [(0, -1), (-1, -1), (-1, 0), (-1, 1)]
        locs = a_to_locs(a)
        
        for i in range(2):
            for j in range(4):
                cnt = [0, 0, 0, 0]
                hy = locs[i] // self._board_size
                hx = locs[i] % self._board_size
                ty = locs[i] // self._board_size
                tx = locs[i] % self._board_size
                dy = direction[j][0]
                dx = direction[j][1]

                for _ in range(6):
                    if ty < 0 or ty >= self._board_size or tx < 0 or tx >= self._board_size:
                        break
                    
                    cnt[s[0][ty][tx]] += 1
                    ty += dy
                    tx += dx

                ty -= dy
                tx -= dx
            
                for k in range(6):
                    if cnt[-s[1][0][0]] == 6:
                        return True
                    
                    cnt[s[0][ty][tx]] -= 1
                    
                    ty -= dy
                    tx -= dx
                    
                    hy -= dy
                    hx -= dx
                    
                    if hy < 0 or hy >= self._board_size or hx < 0 or hx >= self._board_size:
                        break
                    
                    cnt[s[0][hy][hx]] += 1
        
        return False
                   