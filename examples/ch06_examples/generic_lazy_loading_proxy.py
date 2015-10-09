"""
generic_proxy.py - defines a generic lazy loading proxy
"""

from threading import Lock


class LazyLoadingProxy:
    """
    Generic lazy-loading proxy.

    Lazy-loading of the target instance is done by the ProxyMethod helper class.
    """
    def __init__(self, target_class, *args, **kwargs):
        print('LazyLoadingProxy.__init__ called with', str(target_class))
        self.target_class = target_class
        self.target_ctor_args = args
        self.target_ctor_kwargs = kwargs
        self.target = None
        
    def __getattr__(self, name):
        """Called when attribute lookup fails."""
        print('LazyLoadingProxy.__getattr__ called with', name)
        proxy_method = ProxyMethod(self, name)  # ProxyMethod is callable
        setattr(self, name, proxy_method)
        # Because we set the attribute for the proxy method, __getattr__ won't
        # be called the next time the proxy method is referenced. So a reference
        # to a target method, e.g. `get_content`, returns a ProxyMethod 
        # instance whose name is `get_content`.
        return proxy_method


class ProxyMethod:
    """
    A callable class that lazy-loads a target object when a target method is
    called.

    This class is not thread-safe. See ThreadSafeProxyMethod below.
    """
    def __init__(self, proxy, name):
        self.proxy = proxy
        self.name = name
                
    def __call__(self, *args, **kwargs):
        """Called when a ProxyMethod instance is called like a function"""
        if not self.proxy.target:  # if target instance hasn't be created...
            # ...call target class constructor
            self.proxy.target = self.proxy.target_class(
                *self.proxy.target_ctor_args, **self.proxy.target_ctor_kwargs)
        # call target method
        return getattr(self.proxy.target, self.name)(*args, **kwargs)

                
class ThreadSafeProxyMethod:
    """Thread-safe version of ProxyMethod"""
    lock = Lock()
    
    def __init__(self, proxy, name):
        self.proxy = proxy
        self.name = name
                
    def __call__(self, *args, **kwargs):
        """
        Uses the double-check idiom to ensure that another thread doesn't
        initialize the target object between the check for target's existence
        and the lock acquisition.
        """
        if not self.proxy.target:  # check
            with ThreadSafeProxyMethod.lock:  # acquire lock
                if not self.proxy.target:  # double-check
                    # call target class constructor
                    self.proxy.target = self.proxy.target_class(
                        *self.proxy.target_ctor_args,
                        **self.proxy.target_ctor_kwargs)
        # call target method
        return getattr(self.proxy.target, self.name)(*args, **kwargs)


class ConcreteImage:
    def __init__(self, path):
        print('ConcreteImage.__init__ called with', path)
        self.image_content = 'Image content'
        
    def get_content(self):
        print('ConcreteImage.get_content called')
        return self.image_content

    def get_values(self, *args, **kwargs):
        print('ConcreteImage.get_values called with', str(args), str(kwargs))


if __name__ == '__main__':
    dash = '-' * 10
    
    proxy = LazyLoadingProxy(ConcreteImage, '/images/image.jpeg')
    
    print(dash, "calling 'proxy.get_content()'", dash)

    content = proxy.get_content()
    print('call 1 result:', content)

    print(dash, "calling 'proxy.get_content()'", dash)
    
    content = proxy.get_content()
    print('call 1 result:', content)

    print(dash, 'Calling \'proxy.get_values(1, 2, 3, name="Homer")\'', dash)
    
    proxy.get_values(1, 2, 3, name="Homer")

    print(dash, 'Calling \'proxy.get_values()\'', dash)
    
    proxy.get_values()
    
