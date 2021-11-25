def print_greeting(name, end, step):
    for i in range(1, end + 1, step):
        print(f'{i}. Hi, {name}')

print_greeting('Adam', 5, 2)

def square_it(num):
    return num * num

square = square_it(4)
print(f'square is {square}')  # output: square is 16
