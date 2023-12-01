import random
from pprint import pprint
from typing import List, Tuple, Union

from pico_interface import PicoInterface


class RGB:
    LASER = (250, 146, 0)
    MIRROR_LEFT2UP = (196, 4, 4)
    MIRROR_LEFT2DOWN = (0, 255, 0)


class Item:
    LASER = 0
    MIRROR_LEFT2UP = 1
    MIRROR_LEFT2DOWN = 2


class Direction:
    LEFT = 0
    DOWN = 1
    UP = 2
    RIGHT = 3


class LaserGame:
    def __init__(self, max_x: int = 12, max_y: int = 7):
        self.MAX_X = max_x
        self.MAX_Y = max_y
        self.p1_goalpost = [-1 for _ in range(self.MAX_Y)]
        self.p2_goalpost = [-1 for _ in range(self.MAX_Y)]
        self.mirror = [[0] * self.MAX_Y for _ in range(self.MAX_X)]
        self.laser = [[0] * self.MAX_Y for _ in range(self.MAX_X)]
        self.pico_interface = PicoInterface()
        self.RGB = RGB()
        self.Item = Item()
        self.Direction = Direction()
        self.init()
        self.set_goalpost()
        self.send_data = []

    def set_goalpost(self):
        self.p1_goalpost[3] = 0
        self.p2_goalpost[3] = 0
        self.p1_goalpost[random.choice([0, 1, 2, 4, 5, 6])] = 1
        self.p2_goalpost[random.choice([0, 1, 2, 4, 5, 6])] = 1

    def get_goalpost_x(self, user_goalpost_arr: List[int]) -> int:
        return user_goalpost_arr.index(1)

    # 레이저 방향을 바꿔주는 함수
    def mirror_direction(self, x: int, y: int, direction: int) -> int:
        # 거울이 / 일때 방향 설정
        if self.mirror[x][y] == self.Item.MIRROR_LEFT2UP:
            directional_response = {self.Direction.LEFT: self.Direction.DOWN,
                                    self.Direction.DOWN: self.Direction.LEFT,
                                    self.Direction.RIGHT: self.Direction.UP,
                                    self.Direction.UP: self.Direction.RIGHT}
            return directional_response[direction]
        # 거울이 \ 일때 방향 설정
        elif self.mirror[x][y] == self.Item.MIRROR_LEFT2DOWN:
            directional_response = {self.Direction.LEFT: self.Direction.UP,
                                    self.Direction.UP: self.Direction.LEFT,
                                    self.Direction.RIGHT: self.Direction.DOWN,
                                    self.Direction.DOWN: self.Direction.RIGHT}
            return directional_response[direction]

    def dfs(self, x: int, y: int, direction: int) -> Tuple[int, int]:
        if x <= -1 or x >= self.MAX_X:
            return (x + 1, y) if x == -1 else (x - 1, y)
        if y <= -1 or y >= self.MAX_Y:
            return (-1, -1)

        self.laser[x][y] = 1
        if self.mirror[x][y]:
            if self.mirror[x][y] == self.Item.MIRROR_LEFT2UP:
                # print(f'row : {x}, col: {y}, install mirror type /')
                device_id, button_id = self.pico_interface.output_interface(x, y)
                self.send_data.append(dict(
                    c=self.RGB.MIRROR_LEFT2UP,
                    d=device_id,
                    b=button_id
                ))
            elif self.mirror[x][y] == self.Item.MIRROR_LEFT2DOWN:
                # print(f'row : {x}, col: {y}, install mirror type \\')
                device_id, button_id = self.pico_interface.output_interface(x, y)
                self.send_data.append(dict(
                    c=self.RGB.MIRROR_LEFT2DOWN,
                    d=device_id,
                    b=button_id
                ))
            direction = self.mirror_direction(x, y, direction)
        else:
            # print(f'row : {x}, col : {y}, install lazer')
            device_id, button_id = self.pico_interface.output_interface(x, y)
            self.send_data.append(dict(
                c=self.RGB.LASER,
                d=device_id,
                b=button_id
            ))

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
            row[self.MAX_Y // 2] = 1

    def goalin(self, coordinate: Tuple[int, int]):
        row, col = coordinate
        if row == 0 and col != self.get_goalpost_x(self.p1_goalpost):
            self.p1_goalpost[col] = 0
        if row == self.MAX_Y - 1 and col != self.get_goalpost_x(self.p2_goalpost):
            self.p2_goalpost[col] = 0

        if row == 0 and col == self.get_goalpost_x(self.p1_goalpost):
            return dict(result=True, player=2)
        if row == self.MAX_Y - 1 and col == self.get_goalpost_x(self.p2_goalpost):
            return dict(result=True, player=1)
        return dict(result=False, player=0)

    def encode_input(self, mirror_type: str) -> int:
        return self.Item.MIRROR_LEFT2UP if mirror_type == '/' else self.Item.MIRROR_LEFT2DOWN

    def input_mirror(self, row: int, col: int):
        self.mirror[row][col] += 1
        if self.mirror[row][col] > 2:
            self.mirror[row][col] = 0

    # def pprint(self):
    #     print("===========")
    #     for i in self.p1_goalpost:
    #         print("X" if i == -1 else "-" if not i else "X", end=" ")
    #     print(" ")
    #     for i in range(self.MAX_X):
    #         for j in range(self.MAX_Y):
    #             if self.mirror[i][j]:
    #                 print("/" if self.mirror[i][j] == self.Item.MIRROR_LEFT2UP else "\\", end=" ")
    #             else:
    #                 print(self.laser[i][j], end=" ")
    #         print()
    #     for i in self.p2_goalpost:
    #         print("X" if i == -1 else "-" if not i else "X", end=" ")
    #     print(" ")
    #     print("===========")

    def main(self):
        self.send_data = []
        self.dfs(0, self.MAX_Y // 2, self.Direction.DOWN)
        return self.send_data
        # while True:
        #     player = [0]
        #     self.pprint()
        #     cmd = input(f"플레이어{flag} 공격 턴: (install/update/break): ")
        #     if cmd == "install":
        #         x, y, mirror_type = map(str, input().split())
        #         self.input_mirror(int(x), int(y), mirror_type)
        #     elif cmd == "update":
        #         x, y = map(int, input().split())
        #         if self.mirror[x][y] == self.Item.MIRROR_LEFT2UP:
        #             self.input_mirror(x, y, '\\')
        #         else:
        #             self.input_mirror(x, y, '/')
        #     elif cmd == "break":
        #         break
        #     else:
        #         print("다시 입력해주세요")
        #         continue
        #     flag = 2 if flag == 1 else 1
        #     for row in self.laser:
        #         for j in range(self.MAX_Y):
        #             row[j] = 0
        #     result = self.goalin(self.dfs(0, self.MAX_Y // 2, self.Direction.DOWN))
        #     if result['result']:
        #         print(f"플레이어{result['player']}이 승리했습니다!")
        #         break


if __name__ == "__main__":
    laser_game = LaserGame()
    pprint(laser_game.main())
    print('-' * 20)

    laser_game.input_mirror(1, 3)
    pprint(laser_game.main())
    print('-' * 20)

    laser_game.input_mirror(1, 0)
    pprint(laser_game.main())
    print('-' * 20)
