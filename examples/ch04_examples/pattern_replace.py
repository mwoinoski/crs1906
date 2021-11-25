import shutil, re, sys

def replace(file, pattern, repl, ext = 'bak'):
    """ Replace all occurrences of pattern with repl in file """
    try:
        with open(file) as infile, open(f'{file}.tmp', 'w') as outfile:
            outfile.write(re.sub(pattern, repl, infile.read()))
        shutil.copy(file, f'{file}.{ext}')
        shutil.move(f'{file}.tmp', file)
        print('Replace operation succeeded')
    except OSError as ose:
        print(f"Can't replace {pattern} with {repl} in {ose.filename}:",
              ose.strerror)  # message from OS
    except Exception as ex:
        print(f'Error in replace operation: {ex}')

if __name__ == "__main__":
    if len(sys.argv) == 3 or len(sys.argv) == 4:
        replace(*sys.argv[1:])
    else:
        print(f'Usage: {sys.argv[0]} filename pattern repl',
              file=sys.stderr)
