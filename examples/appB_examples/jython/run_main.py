"""Compile and run Main.java"""

import subprocess

env = {'CLASSPATH':
       r'.;C:\python\jython-2.7\jython.jar;C:\python\jython-2.7\PlyJy.jar'}

retcode = subprocess.call(['javac', r'com\ltree\Main.java'], env=env)

if not retcode:
    subprocess.call(['java', r'com.ltree.Main'], env=env)
