import random
from typing import List, Tuple

from util.pico_interface import PicoInterface
from config import RGB
from util.return_class import ReturnClass


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
        print('test:', row, col)
        if row < 0 or row >= self.MAX_ROW:
            if row < 0:
                goalin_result = self.goal_in((row + 1, col))
                self.send_data.append({
                    'player': goalin_result['player'],
                    'result': goalin_result['result'],
                    'row': row + 1,
                    'col': col
                })
            if row >= self.MAX_ROW:
                goalin_result = self.goal_in((row - 1, col))
                self.send_data.append({
                    'player': goalin_result['player'],
                    'result': goalin_result['result'],
                    'row': row - 1,
                    'col': col
                })
            return -1, -1
        if col < 0 or col >= self.MAX_COL:
            if col < 0:
                self.send_data.append({
                    'player': -1,
                    'result': False,
                    'row': row,
                    'col': col + 1
                })
            if col >= self.MAX_COL:
                self.send_data.append({
                    'player': -1,
                    'result': False,
                    'row': row,
                    'col': col - 1
                })
            return -1, -1
        self.laser[row][col] = 1
        if self.mirror[row][col]:
            direction = self.mirror_direction(row, col, direction)
        else:
            device_id, button_id = self.pico_interface.output_interface(row, col)
            self.send_data.append(
                ReturnClass(
                    _color_type='l',
                    _device_id=device_id,
                    _button_id=button_id
                ).get_convert_dict()
            )

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
            return dict(result=False, player=-1)
        if row == self.MAX_ROW - 1 and col != self.get_goalpost_x(self.p2_goalpost):
            self.p2_goalpost[col] = 0
            return dict(result=False, player=-1)
        if row == 0 and col == self.get_goalpost_x(self.p1_goalpost):
            return dict(result=True, player=2)
        if row == self.MAX_ROW - 1 and col == self.get_goalpost_x(self.p2_goalpost):
            return dict(result=True, player=1)
        return dict(result=False, player=-1)

    def input_mirror(self, row: int, col: int):
        self.mirror[row][col] += 1
        if self.mirror[row][col] > 2:
            self.mirror[row][col] = 0

    def goal_check(self):
        _device_id, _button_id = self.send_data[-1]
        row_col = self.pico_interface.output_interface(_device_id, _button_id)
        return self.goal_in(row_col)

    def main(self):

        ##2. 골대 켜진놈들, 현상태 = [턴종료, 골대 꺼진놈들]
        for i in range(7):
            if self.p1_goalpost[i]:
                device_id, button_id = self.pico_interface.output_interface(0, i)
                self.send_data.append(
                    ReturnClass(
                        _color_type='p1',
                        _device_id=device_id,
                        _button_id=button_id
                    ).get_convert_dict()
                )
        for i in range(7):
            if self.p2_goalpost[i]:
                device_id, button_id = self.pico_interface.output_interface(self.MAX_ROW - 1, i)
                self.send_data.append(
                    ReturnClass(
                        _color_type='p2',
                        _device_id=device_id,
                        _button_id=button_id
                    ).get_convert_dict()
                )
        ##3. 거울, 현상태 = [턴종료, 골대 꺼진놈들,거울]

        for row in range(self.MAX_ROW):
            for col in range(self.MAX_COL):
                if self.mirror[row][col]:
                    device_id, button_id = self.pico_interface.output_interface(row, col)
                    self.send_data.append(
                        ReturnClass(
                            _color_type='/' if self.mirror[row][col] == self.Item.MIRROR_LEFT2UP else '\\',
                            _device_id=device_id,
                            _button_id=button_id
                        ).get_convert_dict())

        ##3. 경로1,경로2,...,직전에 꺼진놈, 경로마지막 = [턴종료, 골대 꺼진놈들,거울,경로,꺼진놈,경로]

        self.dfs(0, 3, self.Direction.DOWN)
        return self.send_data
