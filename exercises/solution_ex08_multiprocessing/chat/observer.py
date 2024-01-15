"""
Implementation of the GoF Observer design pattern
"""

__author__ = 'Mike Woinoski (mike@articulatedesign.us.com)'

from abc import ABC, abstractmethod


class Subject(ABC):
    """Subject abstract class."""

    def __init__(self):
        """Initialize set of Observers"""
        self._observers = set()

    @property
    def observers(self):
        return list(self._observers)

    def observer_attach(self, observer, *observers):
        """Add an observers to the list of observers"""
        for observer in (observer,) + observers:
            self._observers.add(observer)

    def observer_detach(self, observer):
        """Remove an Observer from this Subject's set of Observers"""
        self._observers.discard(observer)

    def observer_notify(self, data):
        """Notify all Observers"""
        for observer in self._observers:
            observer.update(data)


class Observer(ABC):
    """Observer interface."""

    def __init__(self, subject=None):
        """Attaches Observer to subject."""
        self.subject = subject
        if subject:
            subject.observer_attach(self)

    @abstractmethod
    def update(self, data):
        pass
