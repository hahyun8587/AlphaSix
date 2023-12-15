def a_to_locs(a: int) -> list:
        if a == -1:
            return [180]
        
        locs = []
        
        for i in range(1, 19 ** 2 - 1):
               if (-i ** 2 + i * 721) / 2 > a:
                   locs.append(i - 1)
                   locs.append(a - (-(i - 1) ** 2 + (i - 1) * 721) // 2 + locs[0] + 1)
                   
                   break
        
        return locs


def move_to_coords(moves: str) -> list:
    if moves == '':
        return []
    
    coords = [] 
    
    for move in moves.split(':'):
        coord = []
      
        coord.append(-int(move[1:]) + 19)
        
        if move[0] <= 'H': 
            coord.append(ord(move[0]) - 65) 
        else:
            coord.append(ord(move[0]) - 66) 
        
        coords.append(coord) 
    
    return coords


def locs_to_a(locs: list) -> int: 
    if len(locs) == 1:
        return -1
    
    if locs[0] < locs[1]:
        a = (-(locs[0] ** 2) + locs[0] * 721) // 2 + locs[1] - locs[0] - 1
    else:
        a = (-(locs[1] ** 2) + locs[1] * 721) // 2 + locs[0] - locs[1] - 1 
    
    return a
    
    