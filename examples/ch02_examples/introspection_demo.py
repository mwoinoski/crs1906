"""
introspection_demo.py - Example of introspection from Chapter 2
"""

def print_docstrings(arg, spacing=20, collapse=True):
    """Print method names and their docstrings."""

    def fmt_str(s):  # local function definition
        return " ".join(s.split()) if collapse else s
        # We could replace this function def with an expression:
        # fmt_str = lambda s: " ".join(s.split()) if collapse else lambda s: s

    method_list = [method for method in dir(arg)
                   if callable(getattr(arg, method))]

    docstrings = ["{} {}".format(method.ljust(spacing),
                                 fmt_str(str(getattr(arg, method).__doc__)))
                  for method in method_list]

    print("\n".join(docstrings))


class MyClass:
    def foo(self):
        """Foo function"""
        pass

    def bar(self):
        """Bar function"""
        pass

print_docstrings(MyClass)

