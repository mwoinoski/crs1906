@echo off
set tempfile=C:\software\cygwin\tmp\path

@rem C and C++ compilers will be C:\software\cygwin\bin\x86_64-w64-mingw32-gcc.exe and *-g++.exe

C:\Python\Python3.7\python.exe -c "import os, re; path=os.environ['PATH']; path=re.sub(r';C:\\[Pp]ython\\pypy;C:\\[Pp]ython\\pypy\\bin', '', path); path=re.sub(r';C:\\[Pp]ython\\jython\\bin', '', path); path=re.sub(r'C:\\software\\mingw32\\bin;C:\\software\\mingw32\\mingw32\\bin;', '', path); path=re.sub(r'Python(.).*?([;\\])', r'Python\1"%1"\2', path); path=re.sub(r';$', '', path); path=re.sub(r'$', r';C:\\Python\\jython\\bin;C:\\Python\\pypy;C:\\python\\pypy\\bin', path); print(path, sep='', end='')" > %tempfile%

set /p PATH= < %tempfile%
path
echo.
python --version
del %tempfile%
prompt $P$_$+$G$S
