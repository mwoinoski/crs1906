class LazyProperty:
    """LazyProperty is a decorator that implements the descriptor protocol
       to implement lazy loading for an attribute.

       Descriptors allow you to override the default behavior of Python's
       attribute access methods: __get__(), __set()__, and __delete__.
       See https://docs.python.org/3/howto/descriptor.html"""
    
    def __init__(self, method):
        self.method = method
        self.method_name = method.__name__
        print('method overriden: {}'.format(self.method))
        print("method's name: {}".format(self.method_name))

    def __get__(self, obj, cls):
        """__get__() is a method of the descriptor protocol.
           When you get an attribute from an object, Python will check if the
           object has a __get__ method. If it does, it will call
           that method and use its return value as the value of the attribute."""
        
        print('in LazyProperty.__get__()')
        if not obj:      # if you're getting a class attribute, obj is None.
            return self  # return the descriptor.
        value = self.method(obj)  # call the decorated method
        print('value after calling self.method(): {}'.format(value))
        
        # Now replace the decorated attribute (a method) with the method's
        # return value. The attribute is no longer a method! It's been
        # transformed into an ordinary data attribute. From this point on,
        # all access of the attribute just return the attribute's value.
        setattr(obj, self.method_name, value)
        return value

class Test:
    def __init__(self):
        self.x = 'foo'
        self.y = 'bar'
        self._resource = None

    @LazyProperty
    def resource(self):
        print('initializing self._resource which is: {}'.format(self._resource))
        self._resource = tuple(range(5)) # expensive initialization goes here
        return self._resource

def main():    
    t = Test()
    print(t.x)
    print(t.y)
    # do more work...
    print('about to access t.resource for the first time')
    print(t.resource)
    print('about to access t.resource for the second time')
    print(t.resource)
    print('about to access t.resource for the third time')
    print(t.resource)

if __name__ == '__main__':
    main()
