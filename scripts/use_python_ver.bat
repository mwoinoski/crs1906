@echo off
set tempfile=C:\cygwin\tmp\path

@rem C compiler will be gcc 64-bit from \cygwin\bin
python -c "import os, re; path=os.environ['PATH']; path=re.sub(r';C:\\python\\jython-2.7\\bin;C:\\python\\pypy;C:\\python\\pypy\\bin', '', path); path=re.sub(r'C:\\software\\mingw32\\bin;C:\\software\\mingw32\\mingw32\\bin;', '', path); path=re.sub(r'python(.).*?([;\\])', r'python\1"%1"\2', path); path=re.sub(r'$', r';C:\\python\\jython-2.7\\bin;C:\\python\\pypy;C:\\python\\pypy\\bin', path); print(path, sep='', end='')" > %tempfile%

set /p PATH= < %tempfile%
path
del %tempfile%
prompt $P$_$+$G
