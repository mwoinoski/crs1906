"""
main.py - Main module of setup_example package.

It's important that this script, which uses the setup_example package, is
defined outside the setup_example packages. Running a script from within
the same package requires some confusing Python options or extra code.
The simplest option is to define scripts outside the packages that they use.
"""

# Note the use of absolute imports. Here, we could use relative imports:
#    from .sample_mod2 import func1
# But the absolute package path seems clearer in this case.
#
# In PyCharm, you need to add setup_example as a source folder.
# File > Settings > Project ch10_examples > Project structure >
#    select setup_example folder > click Sources

from setup_example.sample_mod1 import func1
from setup_example.sample_mod2 import func2


def main():
    print(f"In {__name__}.main()")
    func1()
    func2()


if __name__ == "__main__":
    main()
