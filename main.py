import time
import random
from typing import List, Tuple, Union


class Direction:
    LEFT = 0
    DOWN = 1
    UP = 2
    RIGHT = 3


MAX_X = 7
MAX_Y = 10

MirrorTypeX = 1
MirrorTypeY = 3

# p1_goalpost = [-1 for _ in range(MAX_X)]
# p2_goalpost = [-1 for _ in range(MAX_X)]
p1_goalpost = [-1, -1, -1, 0, 1, -1, -1]
p2_goalpost = [-1, 1, -1, 0, -1, -1, -1]

mirror = [[0] * MAX_X for _ in range(MAX_Y)]
laser = [[0] * MAX_X for _ in range(MAX_Y)]


def get_goalpost_x(user_goalpost_arr: List[int]) -> int:
    for i, val in enumerate(user_goalpost_arr):
        if val == 1:
            return i
    return -1


def mirror_direction(x: int, y: int, direction: Direction) -> Direction:
    if mirror[x][y] == MirrorTypeX:
        return {Direction.LEFT: Direction.DOWN,
                Direction.DOWN: Direction.LEFT,
                Direction.RIGHT: Direction.UP,
                Direction.UP: Direction.RIGHT}[direction]
    if mirror[x][y] == MirrorTypeY:
        return {Direction.LEFT: Direction.UP,
                Direction.UP: Direction.LEFT,
                Direction.RIGHT: Direction.DOWN,
                Direction.DOWN: Direction.RIGHT}[direction]


def dfs(x: int, y: int, direction: Direction) -> Tuple[int, int]:
    if x <= -1 or x >= MAX_Y:
        return (x + 1, y) if x == -1 else (x - 1, y)
    if y <= -1 or y >= MAX_X:
        return (-1, -1)

    laser[x][y] = 1
    if mirror[x][y]:
        direction = mirror_direction(x, y, direction)

    if direction == Direction.LEFT:
        return dfs(x, y - 1, direction)
    elif direction == Direction.RIGHT:
        return dfs(x, y + 1, direction)
    elif direction == Direction.DOWN:
        return dfs(x + 1, y, direction)
    elif direction == Direction.UP:
        return dfs(x - 1, y, direction)
    return (0, 0)


def init():
    for row in laser:
        row[MAX_X // 2] = 1


def goalin(coordinate: Tuple[int, int], player: Union[int, List[int]]) -> bool:
    if coordinate[0] == 0 and coordinate[1] != get_goalpost_x(p1_goalpost):
        p1_goalpost[coordinate[1]] = 0
    if coordinate[0] == MAX_Y - 1 and coordinate[1] != get_goalpost_x(p2_goalpost):
        p2_goalpost[coordinate[1]] = 0

    if coordinate[0] == 0 and coordinate[1] == get_goalpost_x(p1_goalpost):
        player[0] = 2
        return True
    if coordinate[0] == MAX_Y - 1 and coordinate[1] == get_goalpost_x(p2_goalpost):
        player[0] = 1
        return True
    player[0] = -1
    return False


def encode_input(mirror_type: str) -> int:
    return MirrorTypeX if mirror_type == '/' else MirrorTypeY


def input_mirror(x: int, y: int, mirror_type: str):
    mirror[x][y] = encode_input(mirror_type)


def pprint():
    print("===========")
    for i in p1_goalpost:
        print("X" if i == -1 else "-" if not i else "X", end=" ")
    print(" ")
    for i in range(MAX_Y):
        for j in range(MAX_X):
            if mirror[i][j]: print("/" if mirror[i][j] == MirrorTypeX else "\\", end=" ")
            else: print(laser[i][j], end=" ")
        print()
    for i in p2_goalpost:
        print("X" if i == -1 else "-" if not i else "X", end=" ")
    print(" ")
    print("===========")


def main():
    init()
    flag = 1
    while True:
        player = [0]
        pprint()
        cmd = input(f"플레이어{flag} 공격 턴: (install/update/break): ")
        if cmd == "install":
            x, y, mirror_type = map(str, input().split())
            input_mirror(int(x), int(y), mirror_type)
        elif cmd == "update":
            x, y = map(int, input().split())
            if mirror[x][y] == MirrorTypeX:
                input_mirror(x, y, '\\')
            else:
                input_mirror(x, y, '/')
        elif cmd == "break":
            break
        else:
            print("다시 입력해주세요")
            continue
        flag = 2 if flag == 1 else 1
        for row in laser:
            for j in range(MAX_X):
                row[j] = 0
        if goalin(dfs(0, MAX_X // 2, Direction.DOWN), player):
            print(f"플레이어{player[0]}이 승리했습니다!")
            break


if __name__ == "__main__":
    main()
