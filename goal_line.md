def validate_input_for_main(x, y):
    # 거울 설치가 불가능한 행을 정의합니다.
    invalid_rows = [0, 11]

    # 입력된 행이 무효한 행에 해당하는지 확인합니다.
    if x in invalid_rows:
        return False
    else:
        return True

아래의 main함수에서 if cmd == "install": 부분을 다음과 같이 수정한다
        if cmd == "install":
            x, y, mirror_type = map(int, input().split())
            # 입력된 x, y가 유효한지 확인합니다.
            if not validate_input_for_main(x, y):
                continue
elif cmd == "update":
            x, y = map(int, input().split())
            # 입력된 x, y가 유효한지 확인합니다.
            if not validate_input_for_main(x, y):
                continue

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