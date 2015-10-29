"""
template_demo.py - Simplified version of string.Template's metaclass from Chapter 2
"""

import re

class TemplateMetaclass(type):
    default_pattern = 'example' # complex regular expression pattern

    def __init__(cls, name, bases, cls_attrs):
        super().__init__(name, bases, cls_attrs)
        if 'pattern' in cls_attrs:
            pattern = cls.pattern
        else:
            pattern = TemplateMetaclass.default_pattern
        cls.pattern = re.compile(pattern)


class Template(metaclass=TemplateMetaclass):
    """A string class for supporting $-substitutions."""

class MyTemplate(Template):
    pattern = 'This is my template pattern'

my_template = MyTemplate()
print(MyTemplate.pattern)
