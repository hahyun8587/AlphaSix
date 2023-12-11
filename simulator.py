import random

class Gomoku:
    def __init__(self, size=19):
        self.size = size
        self.board = None
        self.player = 1
        self.turn = 0
        self.reset()

    def reset(self):
        self.board = [[0]*self.size for _ in range(self.size)]
        self.player = 1
        self.turn = 0
        # 적돌 배치
        for _ in range(random.randint(1, 5)):
            while True:
                x, y = random.randint(0, self.size-1), random.randint(0, self.size-1)
                if self.is_valid_position(x, y):
                    self.board[x][y] = -1
                    break

    def is_valid_position(self, x, y):
        directions = [(1,0), (0,1), (-1,0), (0,-1), (1,1), (-1,-1), (1,-1), (-1,1)]
        if self.board[x][y] != 0:
            return False
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if nx<0 or nx>=self.size or ny<0 or ny>=self.size:
                continue
            if self.board[nx][ny] != 0:
                return False
        return True
    def notation_to_position(self, notation):
        if ':' in notation:  # 복수 좌표 처리
            return [self.notation_to_position(n) for n in notation.split(':')]

        column, row = notation[0], notation[1:]
        if column.lower() == 'i':  # 'I' 또는 'i'는 무효한 행
            return None
        if not row.isdigit() or not(1 <= int(row) <= 19):  # 줄이 1~19의 정수가 아니면 무효
            return None

        x = ord(column.upper()) - ord('A')
        if x >= 8:  # 'I'를 건너뛰어야 함
            x -= 1
        y = int(row) - 1
        return (x, y)

    def move(self, notation):
        positions = self.notation_to_position(notation)
        if positions is None:  # 좌표가 무효한 경우
            return -1

        for position in positions:
            x, y = position
            if self.board[x][y] == 0:
                self.board[x][y] = self.player

                if self.check_win(x, y):
                    return self.player

                # 게임 시작 후 검은돌(1)은 가운데에만 한번 둘 수 있음
                if self.turn == 0 and self.player == 1 and (x, y) != (self.size//2, self.size//2):
                    return -1

            else:
                return -1

        # 게임 시작 후 각 플레이어는 한 턴에 2개의 돌을 둘 수 있음
        if self.turn > 0:
            self.player = 3 - self.player

        self.turn += 1
        return 0


    def check_win(self, x, y):
        for dx, dy in [(1,0), (0,1), (1,1), (1,-1)]:
            if self.count_stones(x, y, dx, dy) + self.count_stones(x, y, -dx, -dy) - 1 >= 6:
                return True
        return False

    def count_stones(self, x, y, dx, dy):
        count = 0
        while True:
            x += dx
            y += dy
            if x < 0 or x >= self.size or y < 0 or y >= self.size or self.board[x][y] != self.player:
                break
            count += 1
        return count
