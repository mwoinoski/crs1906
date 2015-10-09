def format_args(*args, **kwargs):
    """Formats all arguments into a single string"""
    return ", ".join(str(a) for a in args) + \
        (", " + ", ".join(str(k) + '=' + str(v) for k, v in kwargs.items())
            if kwargs else '')
