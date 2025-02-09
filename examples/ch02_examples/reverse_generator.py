"""
reverse_generator.py - Example of generator function from Chapter 2
"""


def reverse(data):
    index = len(data)
    while index > 0:
        index -= 1
        yield data[index]
    return


print(f'{"-"*10} reverse generator function {"-"*10}')

for char in reverse('golf'):
    print(char)

print(f'{"-"*10} double_it generator function {"-"*10}')


def double_it(data):
    for index in range(0, len(data)):
        yield data[index]


for num in double_it([10, 20, 30, 40]):
    print(num)
