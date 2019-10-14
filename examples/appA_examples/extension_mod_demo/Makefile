# Makefile for Linux
# Default goal is all
# Run GNU's make command from a command prompt:
#    make

COMPILER=gcc
#COMPILER=mingw32
PYTHON=python
RM=rm -rf
.PHONY: all clean extmod

all: clean extmod

extmod:
	$(PYTHON) setup.py build_ext --inplace --compiler=$(COMPILER)

# '-' before command causes errors not to exit the process
clean:
	-$(RM) $(OBJ) $(DLL) *.pyd __pycache__ build core
