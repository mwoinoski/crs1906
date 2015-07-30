"""
Implementation of the GoF Observer design pattern
"""

__author__ = 'Mike Woinoski (michaelw@articulatedesign.us.com)'

from abc import ABCMeta, abstractmethod


class Observer(metaclass=ABCMeta):
    """Observer interface"""
    @abstractmethod
    def notify(self, observable):
        pass


class Observable(metaclass=ABCMeta):
    """Observable abstract class

    May be used as a base class or a mixin
    """
    def __init__(self):
        """Initializes list of observers"""
        self._observers = []

    def add_observer(self, observer):
        """Adds an observers to the list of observers"""
        if observer not in self._observers:
            self._observers.append(observer)
        return self

    def notify_observers(self):
        """Notify all observers"""
        for observer in self._observers:
            observer.notify(self)
        return self
