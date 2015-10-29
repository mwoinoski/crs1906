"""
jython_demo.py - Jython demo from chapter 7
"""

from java.util import Date  # import Java's standard Date class

from com.ltree import HelloWorld  # import a custom Java class

from time import sleep  # Python's sleep

d1 = Date()  # instantiate Java Date

sleep(1.0)

d2 = Date()

if d1 < d2:  # compare with Python operators
    print "%s < %s" % (str(d1), str(d2))

if d2 > d1:
    print "%s > %s" % (str(d2), str(d1))

h = HelloWorld()  # instantiate custom Java class

h.hello()         # call Java method

h.hello("Python")  # overloaded methods work too

