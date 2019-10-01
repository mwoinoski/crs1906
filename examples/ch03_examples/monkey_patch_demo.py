r"""
monkey_patch_demo.py - Example of monkey patching, from Chapter 3
"""

class SimpleCounter:
	def __init__(self, start=0):
		self.count = start
	
	def increment(self, incr=1):
		self.count += incr
	
def debug_incr(obj, incr=1):
	obj.count += incr
	print('new value =', obj.count)

counter = SimpleCounter()

print('\nCalling counter.increment() before monkey patch:')
counter.increment()
	
SimpleCounter.increment = debug_incr

print('\nCalling counter.increment() after monkey patch:')
counter.increment()

