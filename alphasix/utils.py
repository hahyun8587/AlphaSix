from math import sqrt, floor

def atoc(a: int, n: int) -> tuple:
    """Converts action `a` into the corresponding pairs of coordinate.  

    The coordinate is indices of 2D array which represents the board. 

    Args:
        a (int): The action to be converted.
        n (int): The size of the board.
        
    Raises: 
        ValueError: Raises when `a` is smaller than `0` or bigger than 
            max action. Max action is calculated as 
            `n x n x (n x n - 1) / 2 - 1`.
    """
    
    if a < 0 or a > n * n * (n * n - 1) / 2 - 1:
        raise ValueError('action out of range.')

    i = floor((2 * n * n + 1 
               - sqrt((2 * n * n + 1) ** 2 -  4 * (2 * n * n + 2 * a))) / 2)    
    locs = [i - 1, a + 1 + i * (i + 1) // 2 - 1 + (i - 1) * -n * n]

    return tuple((loc // n, loc % n) for loc in locs) 

    
