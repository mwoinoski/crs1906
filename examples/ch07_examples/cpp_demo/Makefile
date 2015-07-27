# Makefile
# Run make from MinGW:
#    mingw32-make all

SRC=primes_c.c primes_main.c
OBJ=$(SRC:.c=.o) # replaces the .c from SRC with .o
EXE=primes_main.exe

CC=gcc
CFLAGS=-Wall -O3 -g
LDFLAGS=-mwindows
RM=rm -f
.PHONY: all clean

%.o: %.c         # combined w/ next line will compile recently changed .c files
	$(CC) $(CFLAGS) -o $@ -c $<

all: $(EXE)      # all is dependent on $(EXE) to be complete

$(EXE): $(OBJ)   # $(EXE) is dependent on all of the files in $(OBJ) to exist
	$(CC) $(OBJ) $(LDFLAGS) -o $@

# '-' causes errors not to exit the process
clean:
	-$(RM) $(OBJ) $(EXE) core
