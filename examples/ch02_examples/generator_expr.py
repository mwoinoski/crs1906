"""
generator_expr.py - Example of generator expressions from Chapter 1
"""

powers = [2, 4, 8, 16, 32]
msg = ", ".join(str(p) for p in powers)
print("msg = {}".format(msg))

graduates = [
    ('Paul', 3.0),
    ('George', 2.0),
    ('Ringo', 1.0),
    ('John', 4.0),
]

top = max((grad[1], grad[0]) for grad in graduates)

print("top graduate = {}".format((top[1], top[0])))
