"""
Implementation of the GoF Observer design pattern
"""

__author__ = 'Mike Woinoski (mike@articulatedesign.us.com)'

from abc import ABCMeta, abstractmethod


class Subject(metaclass=ABCMeta):
    """Subject abstract class."""

    def __init__(self):
        """Initialize set of Observers"""
        self._observers = set()

    @property
    def observers(self):
        return list(self._observers)

    def observer_attach(self, obs, *observers):
        """Add an observers to the list of observers"""
        for obs in (obs,) + observers:
            self._observers.add(obs)

    def observer_detach(self, observer):
        """Remove an Observer from this Subject's set of Observers"""
        self._observers.discard(observer)

    def observer_notify(self, data):
        """Notify all Observers"""
        for obs in self._observers:
            obs.update(data)


class Observer(metaclass=ABCMeta):
    """Observer interface."""

    def __init__(self, subject=None):
        """Attaches Observer to subject."""
        self.subject = subject
        if subject:
            subject.observer_attach(self)

    @abstractmethod
    def update(self, data):
        pass
