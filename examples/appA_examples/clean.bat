@echo off
@rem Windows doesn't expand wildcards for Cygwin commands, so use del for files and rm for directories
del hello.c integrate.c primes_c_wrapper.c primes_cython.c *.pyd *.o *.exe *.dll *.a 2>nul
rm -fr __pycache__ build 2>nul
ls
