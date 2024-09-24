# Python basic features review

# Function Definitions

# TODO: Create a function calculate_area that takes the radius of a circle as a 
# parameter and returns its area. Use the formula area = pi * radius**2. Test
# your function with a radius of 7.0
# HINT: for the value of pi, import math, then reference math.pi
# HINT: to run this file: PyCharm Run menu > Run > python_basics_review
#       OR Ctrl-Shift-F10

import math


def calculate_area(radius):
    return math.pi * radius**2


area = calculate_area(7.0)
print(f'area of a circle with radius 7.0 is {area:.3f}')

# TODO: Write a function find_max that takes a list of numbers as an argument 
# and returns the maximum number in that list without using the built-in max() 
# function. The numbers in the input list may be positive, negative, or zero.
# HINT: initialize a variable to negative infinity using this expression:
#   float('-inf')


def max_num(nums):
    max_so_far = float('-inf')
    for num in nums:
        if num > max_so_far:
            max_so_far = num
    return max_so_far


print(f'maximum of [10.1] is {max_num([10.1])}')
print('maximum of [40.4, 30.33, 20, 10.1] is '
      f'{max_num([40.4, 30.33, 20, 10.1])}')
print('maximum of [-40.4, 30.33, 20, 10.1] is '
      f'{max_num([-40.4, 30.33, 20, 10.1])}')
print('maximum of [-40.4, -30.33, -20, -10.1] is '
      f'{max_num([-40.4, -30.33, -20, -10.1])}')
print('maximum of [20, 10.1, 40.4, 10.1] is '
      f'{max_num([20, 10.1, 40.4, 10.1])}')

# F-Strings

# TODO: Write a function greet that takes a name and an age as parameters and 
# returns a greeting string using f-strings. For example, greet("Alice", 30)
# should return "Hello Alice, you are 30 years old!".
# HINT: see slide 1-8


def greet(name, age):
    return f'Hello {name}, you are {age} years old!'


message = greet('Alice', 30)
print(message)

# TODO: Write a function format_product that takes two parameters, product_name 
# and price, and returns a string using f-strings, formatted like this: 
#   Product: [product_name], Price: $[price]
# The price should be rounded to two decimal places. For instance,
# format_product("Book", 15.987) should return:
#   Product: Book, Price: $15.99


def format_product(product_name, price):
    return f'Product: {product_name}, Price: ${price:.2f}'


result = format_product('Book', 15.987)
print(result)

# String Operations and List Comprehensions

title = ['to', 'kill', 'a', 'mockingbird']
# TODO: Read the following code and be sure you understand it. Then write a
# list comprehension that replaces the `for` loop:
#   capitalized = []
#   for word in title:
#       capitalized.append(word[0].upper() + word[1:])
#   print(capitalized)

capitalized = [word[0].upper() + word[1:] for word in title]
print(capitalized)

# TODO: Write a list comprehension that generates a list of squares for all 
# even numbers between 1 and 20. The output should be:
#   [4, 16, 36, 64, 100, 144, 196, 256, 324, 400]

squares_of_evens = [num**2 for num in range(1, 20) if num % 2 == 0]
print(squares_of_evens)

# BONUS EXERCISES

# TODO: Write a function div_by_3_and_5 that finds all the numbers in a given
# range that are divisible by 3 and 5. The function should return a list of 
# these numbers. For instance, div_by_3_and_5(1, 90) should return 
# [15, 30, 45, 60, 75, 90]
# Generate the list using a list comprehension.
# HINT: use the built-in range() function to generate a sequence of numbers.
# See slide 1-11


def multiples_of_3_and_5(start, end):
    return [n for n in range(start, end + 1)
            if n % 3 == 0 and n % 5 == 0]


result = multiples_of_3_and_5(1, 90)
print(f'multiples of 3 and 5 in the range 1 to 90: {result}')

# TODO: Create a list comprehension that takes a list of strings and generates
# a new list containing the length of each string. Test this with the list
# ["apple", "banana", "cherry", "date"]

strings = ["apple", "banana", "cherry", "date"]
lengths = [len(s) for s in strings]
print(lengths)

# Dict Comprehensions

# TODO: Create a dict comprehension that generates a dictionary where the keys
# are numbers from 1 to 10 and the values are the cubes of these numbers. The
# result should be {1: 1, 2: 8, 3: 27, ..., 10: 1000}

cubes = {n: n**3 for n in range(1, 11)}
print(cubes)

# TODO: Write a dict comprehension that inverts a dictionary (swaps its keys
# and values). Start with a predefined dictionary, such as:
#   {'a': 1, 'b': 2, 'c': 3}
# and generate a new dictionary where it becomes {1: 'a', 2: 'b', 3: 'c'}

input_dict = {'a': 1, 'b': 2, 'c': 3}
output_dict = {input_dict[k]: k for k in input_dict}
# this works too:
#   output_dict = {v: k for k, v in input_dict.items()}
print(f'output_dict = {output_dict}')
