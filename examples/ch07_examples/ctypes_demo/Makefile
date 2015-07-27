# Makefile
# Default goal is all
# Run MinGW's make command from a command prompt:
#    make

SRC=primes.c
OBJ=$(SRC:.c=.o) # replaces the .c from SRC with .o
DLL=primes.dll

CC=gcc
CFLAGS=-DBUILDING_PRIMES_DLL -Wall -Og -g
LDFLAGS=-shared
RM=rm -f
.PHONY: all clean

all: clean $(DLL)      # all is dependent on $(DLL) to be complete

%.o: %.c         # combined w/ next line will compile recently changed .c files
	$(CC) $(CFLAGS) -o $@ -c $<

$(DLL): $(OBJ)   # $(DLL) is dependent on all of the files in $(OBJ) to exist
	$(CC) $(OBJ) $(LDFLAGS) -o $@

# '-' before command causes errors not to exit the process
clean:
	-$(RM) $(OBJ) $(DLL) __pycache__ build core
