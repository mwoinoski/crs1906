@echo off

set tempfile=C:\cygwin\tmp\path

call use_python_ver Python3.3-x86

@rem Add mingw32 gcc compiler to start of PATH, to hide cygwin 64-bit gcc
python -c "import os, re; print(re.sub(r'^', r'C:\\software\\mingw32\\bin;C:\\software\\mingw32\\mingw32\\bin;', os.environ['PATH']), sep='', end='')" > %tempfile%

set /p PATH= < %tempfile%
echo.
path
del %tempfile%


