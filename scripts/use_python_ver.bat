@echo off
set tempfile=C:\cygwin\tmp\path

python -c "import os, re; print(re.sub(r'python-.*?([;\\])', r'python-"%1"\1', os.environ['PATH']))" > %tempfile%

set /p PATH= < %tempfile%

path

del %tempfile%