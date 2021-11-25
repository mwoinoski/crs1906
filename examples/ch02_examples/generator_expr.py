"""
generator_expr.py - Example of generator expressions from Chapter 2
"""

powers = [2, 4, 8, 16, 32]
msg = ", ".join(str(p) for p in powers)
print(f"msg = {msg}")

graduates = [
    ('Paul', 3.0),
    ('George', 2.0),
    ('Ringo', 1.0),
    ('John', 4.0),
]

top = max((grad[1], grad[0]) for grad in graduates)

print(f"top graduate = {(top[1], top[0])}")
