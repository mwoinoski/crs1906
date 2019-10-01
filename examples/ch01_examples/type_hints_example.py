#!/usr/bin/python3.7
# Example: py type_hints.py

def stringify(num: int) -> str:
    return str(num)


def plus(num1: int, num2: int) -> int:
    return num1 + num2


def f(num1: int, my_float: float = 3.5) -> float:
    return num1 + my_float


def print_sum(num1: int, num2: int) -> None:
    print(f"{num1} + {num2} = {plus(num1, num2)}")


print_sum(11, 22)

print(f(99, 3.1415))

result = stringify('one')
print(result)
