import random
from pprint import pprint
from typing import List, Tuple, Union

from pico_interface import PicoInterface
from config import RGB


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
    def __init__(self, MAX_ROW: int = 12, MAX_COL: int = 7):
        self.MAX_ROW = MAX_ROW
        self.MAX_COL = MAX_COL
        self.p1_goalpost = [-1 for _ in range(self.MAX_COL)]
        self.p2_goalpost = [-1 for _ in range(self.MAX_COL)]
        self.mirror = None
        self.laser = None
        self.pico_interface = PicoInterface()
        self.RGB = RGB()
        self.Item = Item()
        self.Direction = Direction()
        self.init()
        self.send_data = []

    def set_goalpost(self):
        self.p1_goalpost[3] = 0
        self.p2_goalpost[3] = 0
        self.p1_goalpost[random.choice([0, 1, 2, 4, 5, 6])] = 1
        self.p2_goalpost[random.choice([0, 1, 2, 4, 5, 6])] = 1

    def get_goalpost_x(self, user_goalpost_arr: List[int]) -> int:
        return user_goalpost_arr.index(1)

    # 레이저 방향을 바꿔주는 함수
    def mirror_direction(self, row: int, col: int, direction: int) -> int:
        # 거울이 / 일때 방향 설정
        if self.mirror[row][col] == self.Item.MIRROR_LEFT2UP:
            directional_response = {self.Direction.LEFT: self.Direction.DOWN,
                                    self.Direction.DOWN: self.Direction.LEFT,
                                    self.Direction.RIGHT: self.Direction.UP,
                                    self.Direction.UP: self.Direction.RIGHT}
            return directional_response[direction]
        # 거울이 \ 일때 방향 설정
        elif self.mirror[row][col] == self.Item.MIRROR_LEFT2DOWN:
            directional_response = {self.Direction.LEFT: self.Direction.UP,
                                    self.Direction.UP: self.Direction.LEFT,
                                    self.Direction.RIGHT: self.Direction.DOWN,
                                    self.Direction.DOWN: self.Direction.RIGHT}
            return directional_response[direction]

    def dfs(self, row: int, col: int, direction: int) -> Tuple[int, int]:
        if row <= -1 or row >= self.MAX_ROW:
            return (row + 1, col) if row == -1 else (row - 1, col)
        if col <= -1 or col >= self.MAX_COL:
            return -1, -1

        self.laser[row][col] = 1
        if self.mirror[row][col]:
            direction = self.mirror_direction(row, col, direction)
        else:
            device_id, button_id = self.pico_interface.output_interface(row, col)
            self.send_data.append(dict(
                c='l',
                d=device_id,
                b=button_id
            ))

        if direction == self.Direction.LEFT:
            return self.dfs(row, col - 1, direction)
        elif direction == self.Direction.RIGHT:
            return self.dfs(row, col + 1, direction)
        elif direction == self.Direction.DOWN:
            return self.dfs(row + 1, col, direction)
        elif direction == self.Direction.UP:
            return self.dfs(row - 1, col, direction)
        return 0, 0

    def init(self):
        self.mirror = [[0] * self.MAX_COL for _ in range(self.MAX_ROW)]
        self.laser = [[0] * self.MAX_COL for _ in range(self.MAX_ROW)]
        for row in self.laser:
            row[self.MAX_COL // 2] = 1
        self.set_goalpost()

    def goal_in(self, coordinate: Tuple[int, int]):
        row, col = coordinate
        if row == 0 and col != self.get_goalpost_x(self.p1_goalpost):
            self.p1_goalpost[col] = 0
        if row == self.MAX_COL - 1 and col != self.get_goalpost_x(self.p2_goalpost):
            self.p2_goalpost[col] = 0

        if row == 0 and col == self.get_goalpost_x(self.p1_goalpost):
            return dict(result=True, player=2)
        if row == self.MAX_COL - 1 and col == self.get_goalpost_x(self.p2_goalpost):
            return dict(result=True, player=1)
        return dict(result=False, player=-1)

    def input_mirror(self, row: int, col: int):
        self.mirror[row][col] += 1
        if self.mirror[row][col] > 2:
            self.mirror[row][col] = 0

    def goal_check(self):
        row_col = self.pico_interface.output_interface(self.send_data[-1]['d'], self.send_data[-1]['b'])
        return self.goal_in(row_col)

    def main(self):
        self.send_data = []
        self.dfs(0, self.MAX_COL // 2, self.Direction.DOWN)
        return self.send_data


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
