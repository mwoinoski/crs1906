"""
scratch.py - scratch script
"""

__author__ = 'user'

import json

s = '{"type":"music", "url":"localhost"}'
obj = json.loads(s)
print(obj['type'] + " " + obj['url'])