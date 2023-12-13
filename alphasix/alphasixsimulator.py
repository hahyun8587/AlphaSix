import numpy as np
from tools.AlphaZero.alphazero.simulator import Simulator

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
        locs = self._a_to_locs(a)
        
        next_s[0][locs[0] // self._board_size][locs[0] % self._board_size] = s[1][0][0]
        next_s[0][locs[1] // self._board_size][locs[1] % self._board_size] = s[1][0][0]
        next_s[1].fill(-s[1][0][0])
        
        return next_s
    
    
    def is_terminal(self, s: np.ndarray, a: int) -> int:
        direction = [(0, -1), (-1, -1), (-1, 0), (-1, 1)]
        locs = self._a_to_locs(a)
        
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
                        return -1
                    
                    cnt[s[0][ty][tx]] -= 1
                    
                    ty -= dy
                    tx -= dx
                    
                    hy -= dy
                    hx -= dx
                    
                    if hy < 0 or hy >= self._board_size or hx < 0 or hx >= self._board_size:
                        break
                    
                    cnt[s[0][hy][hx]] += 1
        
        return 0
                

    def _a_to_locs(self, a: int) -> list:
        locs = [-1, -1]
        
        for i in range(1, self._board_size ** 2 - 1):
               if (-i ** 2 + i * 721) / 2 > a:
                   locs[0] = i - 1
                   locs[1] = a - ((i - 1) ** 2 + (i - 1) * 721) + locs[0] + 1
                   
                   break
        
        return locs
                   