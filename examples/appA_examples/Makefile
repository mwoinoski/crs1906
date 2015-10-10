# Makefile
# Default goal is all
# GNU make is installed under \cygwin\bin.
# To build the DLL for primes, run "make" from a command prompt:
#    make

SRC=primes_c.c primes_main.c
OBJ=$(SRC:.c=.o) # replaces the .c from SRC with .o
EXE=primes_main.exe

CC=gcc
CFLAGS=-Wall -Og -g
LDFLAGS=-mwindows
RM=rm -rf
.PHONY: all clean

%.o: %.c         # combined w/ next line will compile recently changed .c files
	$(CC) $(CFLAGS) -o $@ -c $<

all: $(EXE)      # all is dependent on $(EXE) to be complete

$(EXE): $(OBJ)   # $(EXE) is dependent on all of the files in $(OBJ) to exist
	$(CC) $(OBJ) $(LDFLAGS) -o $@

# '-' before command causes errors not to exit the process
clean:
	-$(RM) $(OBJ) $(DLL) __pycache__ build core
