"""
generator_expr.py - Example of generator expressions from Chapter 1
"""

import csv


class Student:
    def __init__(self, name, gpa):
        self.name = name
        self.gpa = gpa


populations = [36000000, 10000000, 65000000, 321000000]
msg = ", ".join(str(p) for p in populations)
print("msg = {}".format(msg))

graduates = [
    Student('B', 3.0),
    Student('C', 2.0),
    Student('D', 1.0),
    Student('A', 4.0),
]

top = max((student.gpa, student.name) for student in graduates)

print("top graduate = {}".format((top[1], top[0])))

# Read student data from CSV file
with open('students.csv', newline='') as csv_file:
    student_reader = csv.reader(csv_file)
    next(student_reader)  # skip header line
    # csv.reader objects are iterable, so we can use them
    # directly in list comprehensions and generator expressions
    grads = [Student(row[0], row[1]) for row in student_reader]

top = max((student.gpa, student.name) for student in grads)

print("top grad = {}".format((top[1], top[0])))
