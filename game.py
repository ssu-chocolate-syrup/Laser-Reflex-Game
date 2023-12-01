from typing import List, Tuple, Union

class LaserGame:
    class Direction:
        LEFT = 0
        DOWN = 1
        UP = 2
        RIGHT = 3

    def __init__(self, max_x: int = 10, max_y: int = 7):
        self.MAX_X = max_x
        self.MAX_Y = max_y
        self.MirrorTypeX = 1
        self.MirrorTypeY = 3
        self.p1_goalpost = [-1 for _ in range(self.MAX_Y)]
        self.p2_goalpost = [-1 for _ in range(self.MAX_Y)]
        self.p1_goalpost[3] = 0
        self.p2_goalpost[3] = 0
        self.mirror = [[0] * self.MAX_Y for _ in range(self.MAX_X) ]
        self.laser = [[0] * self.MAX_Y for _ in range(self.MAX_X)]

    def get_goalpost_x(self, user_goalpost_arr: List[int]) -> int:
        for i, val in enumerate(user_goalpost_arr):
            if val == 1:
                return i
        return -1

    def mirror_direction(self, x: int, y: int, direction: "LaserGame.Direction") -> "LaserGame.Direction":
        if self.mirror[x][y] == self.MirrorTypeX:
            return {self.Direction.LEFT: self.Direction.DOWN,
                    self.Direction.DOWN: self.Direction.LEFT,
                    self.Direction.RIGHT: self.Direction.UP,
                    self.Direction.UP: self.Direction.RIGHT}[direction]
        if self.mirror[x][y] == self.MirrorTypeY:
            return {self.Direction.LEFT: self.Direction.UP,
                    self.Direction.UP: self.Direction.LEFT,
                    self.Direction.RIGHT: self.Direction.DOWN,
                    self.Direction.DOWN: self.Direction.RIGHT}[direction]

    def dfs(self, x: int, y: int, direction: "LaserGame.Direction") -> Tuple[int, int]:
        if x <= -1 or x >= self.MAX_Y:
            return (x + 1, y) if x == -1 else (x - 1, y)
        if y <= -1 or y >= self.MAX_X:
            return (-1, -1)
        self.laser[x][y] = 1
        if self.mirror[x][y]:
            if self.mirror[x][y] == 1:
                print(f'row : {x}, col: {y}, install mirror type /')
            else:
                print(f'row : {x}, col: {y}, install mirror type \\')
            direction = self.mirror_direction(x, y, direction)
        else:
            print(f'row : {x}, col : {y}, install lazer')
        if direction == self.Direction.LEFT:
            return self.dfs(x, y - 1, direction)
        elif direction == self.Direction.RIGHT:
            return self.dfs(x, y + 1, direction)
        elif direction == self.Direction.DOWN:
            return self.dfs(x + 1, y, direction)
        elif direction == self.Direction.UP:
            return self.dfs(x - 1, y, direction)
        return (0, 0)

    def init(self):
        for row in self.laser:
            row[self.MAX_Y//2] = 1

    def goalin(self, coordinate: Tuple[int, int], player: Union[int, List[int]]) -> bool:
        if coordinate[0] == 0 and coordinate[1] != self.get_goalpost_x(self.p1_goalpost):
            self.p1_goalpost[coordinate[1]] = 0
        if coordinate[0] == self.MAX_Y - 1 and coordinate[1] != self.get_goalpost_x(self.p2_goalpost):
            self.p2_goalpost[coordinate[1]] = 0
        if coordinate[0] == 0 and coordinate[1] == self.get_goalpost_x(self.p1_goalpost):
            player[0] = 2
            return True
        if coordinate[0] == self.MAX_Y - 1 and coordinate[1] == self.get_goalpost_x(self.p2_goalpost):
            player[0] = 1
            return True
        player[0] = -1
        return False

    def encode_input(self, mirror_type: str) -> int:
        return self.MirrorTypeX if mirror_type == '/' else self.MirrorTypeY

    def input_mirror(self, x: int, y: int, mirror_type: str):
        self.mirror[x][y] = self.encode_input(mirror_type)

    def pprint(self):
        print("===========")
        for i in self.p1_goalpost:
            print("X" if i == -1 else "-" if not i else "X", end=" ")
        print(" ")
        for i in range(self.MAX_X):
            for j in range(self.MAX_Y):
                if self.mirror[i][j]:
                    print("/" if self.mirror[i][j] == self.MirrorTypeX else "\\", end=" ")
                else:
                    print(self.laser[i][j], end=" ")
            print()
        for i in self.p2_goalpost:
            print("X" if i == -1 else "-" if not i else "X", end=" ")
        print(" ")
        print("===========")

    def main(self):
        self.init()
        flag = 1
        while True:
            player = [0]
            self.pprint()
            cmd = input(f"플레이어{flag} 공격 턴: (install/update/break): ")
            if cmd == "install":
                x, y, mirror_type = map(str, input().split())
                self.input_mirror(int(x), int(y), mirror_type)
            elif cmd == "update":
                x, y = map(int, input().split())
                if self.mirror[x][y] == self.MirrorTypeX:
                    self.input_mirror(x, y, '\\')
                else:
                    self.input_mirror(x, y, '/')
            elif cmd == "break":
                break
            else:
                print("다시 입력해주세요")
                continue
            flag = 2 if flag == 1 else 1
            for row in self.laser:
                for j in range(self.MAX_X):
                    row[j] = 0
            if self.goalin(self.dfs(0, self.MAX_X // 2, self.Direction.DOWN), player):
                print(f"플레이어{player[0]}이 승리했습니다!")
                break

if __name__ == "__main__":
    laser_game = LaserGame()
    laser_game.main()