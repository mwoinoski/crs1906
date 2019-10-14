# Makefile
# Default goal is all
# Run MinGW's make command from a command prompt:
#    make

COMPILER=mingw32
PYTHON=python
RM=rm -rf
.PHONY: all reminder clean extmod

all: reminder clean extmod

reminder:
	@echo
	@echo "****** Did you run use_python33x86 ? ******"
	@echo

extmod:
	@echo
	$(PYTHON) setup.py build_ext --inplace --compiler=$(COMPILER)
	@echo

# '-' before command causes errors not to exit the process
clean:
	-$(RM) $(OBJ) $(DLL) *.c *.pyd __pycache__ build core
