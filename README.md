# Git 커밋 메세지 규칙
`git commit`을 하기 전에, 커밋 메세지를 아래와 같은 포맷으로 작성해주세요. 어떤 내용을 수정해서 커밋을 했는지, 한 번에 알아보기 쉽게 하기 위함입니다.

`<type>: <title>`

- `<type>`에는 아래에서 선택하여 작성합니다.
    - feat: 새로운 기능 추가
    - fix: 버그 수정
    - refactor: 코드 리팩토링
    - style: 코드 스타일 변경 혹은 코드 정렬 (코드에 직접적인 수정이 없을 때)
    - docs: 문서 변경
    - test: 테스트 코드 추가 및 변경
    - chore: 배포 환경 수정

- `<title>`에는 아래의 규칙을 지켜서 작성해주세요.
    - 타이틀 첫 번째 글자는 무조건 대문자로 적어주세요.
    - 타이틀 맨 마지막에 마침표를 사용하지 마세요.
    - 타이틀은 단순하게, 명령조로 작성해주세요. (ex. ✅: Using staticmethod, 😵: The staticmethod was used.)


# 파이썬 코드 규칙

1. 들여쓰기를 할 때 Tab 대신 공백(Space)을 사용한다. 특히 Python 3는 Tab과 공백을 혼용해서 사용하는 것을 허용하지 않는다.

2. 문법적으로 들여쓰기를 할 때는 4개의 공백을 사용한다.

3. import는 (여러 모듈을 콤마로 연결하지 말고) 한 라인에 하나의 모듈을 import한다.

```python
# ✅
import os
import sys

# 💩
import os, sys
```

4. 함수 호출, 함수 파라미터 등에서 불필요한 공백을 넣지 않는다.
```python
# ✅
foo(1+2*2)
foo(ham[1], {eggs: 2})
bar = (0,)
foo(1)

# 💩
foo(1 + 2 * 2)
foo( ham[ 1 ], { eggs: 2 } )
bar = (0, )
foo (1)
```

5. 변수 할당시 할당자 앞뒤로 하나의 공백만 넣는다.
```python
# ✅
i = i + 1

# 💩
i=i+1
```

6. 함수, 변수는 소문자로 단어 간은 밑줄(_)을 사용하여 연결한다. (snake_case로 변수명을 짜자. class는 CamelCase로!)
```python
# ✅
def make_array(arg_main, arg_sub):
    pass

# 💩
def makeArray(argMain, argSub):
    pass
```

7. 함수, 변수의 이름은 항상 추상적이지 않고 바로 이해가 되게끔 적는다.
```python
# ✅
ONE_DAY_SEC = 60 * 60 * 24

def get_id():
    pass

# 💩
x = 86400

def f():
    pass
```

8. 상수인 변수는 모두 대문자로 적는다.
```python
# ✅
ONE_DAY_SEC = 60 * 60 * 24

# 💩
one_day_sec = 60 * 60 * 24
```

9. 코드의 주석은 항상 코드 위에 적도록 하자
```python
# ✅
# 문자열 변수인 user_id를 받아 해당 아이디가 DB에 몇 번째로 저장되어 있는지 확인하는 함수이다.
def get_username(user_id: str):
    for idx, value in enumerate(user_db):
        # 반복문을 돌다가 value.id가 user_id와 같은 원소를 찾았다면, 인덱스를 호출한다. 
        if value.id == user_id:
            print(f'{idx}번째 아이디입니다.')
```