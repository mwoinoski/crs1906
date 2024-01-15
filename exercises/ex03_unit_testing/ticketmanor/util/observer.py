"""
Implementation of the GoF Observer design pattern
"""

__author__ = 'Mike Woinoski (mike@articulatedesign.us.com)'

from abc import ABC, abstractmethod


class Observer(ABC):
    """
    Observer interface
    """
    @abstractmethod
    def update(self, observable):
        """ Subject calls update to notify an Observer of a change of state """


class Subject(ABC):
    """
    Subject abstract class.

    May be used as a base class or a mixin.
    """

    def __init__(self):
        """Initialize set of Observers"""
        self._observers = set()

    def observer_attach(self, observer, *observers):
        """Add an observers to the list of observers"""
        for observer in (observer,) + observers:
            if observer not in self._observers:
                self._observers.add(observer)
                observer.update(self)
                # Observer gets current value of Subject
        return self
        # if observers is potentially a very large collection,
        # use itertools.chain() instead of tuple concatenation:
        #   for observer in itertools.chain((observer,), observers):

    def observer_detach(self, observer):
        """Remove an Observer from this Subject's set of Observers"""
        self._observers.discard(observer)
        return self

    def observer_notify(self):
        """Notify all Observers"""
        for observer in self._observers:
            observer.update(self)
        return self
