"""
observer.py - Example of Observer design pattern.
"""

from abc import ABCMeta, abstractmethod
import itertools


class Subject(metaclass=ABCMeta):
    def __init__(self):
        self._observers = set()

    def observer_attach(self, obs, *observers):
        for obs in (obs,) + observers:
            self._observers.add(obs)
            obs.update(self)  # observer gets current value of observered

        # if observers is potentially a very large collection,
        # use itertools.chain() instead of tuple concatentation:
        #   for observer in itertools.chain((observer,), observers):

    def observer_detach(self, observer):
        self._observers.discard(observer)

    def observer_notify(self):
        for obs in self._observers:
            obs.update(self)


class Observer(metaclass=ABCMeta):
    @abstractmethod
    def update(self, observable):
        pass


class ConcreteSubject(Subject):
    def __init__(self, value=None):
        super().__init__()
        self._state = None  # _value must be set before setter is invoked
        self.state = value  # invoke property setter

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        if self._state != value:
            self._state = value
            self.observer_notify()


class ConcreteObserver(Observer):
    def __init__(self, name):
        super().__init__()
        self._name = name

    def update(self, subject):
        print('{}.update() called, subject state = {}'
              .format(self._name, subject.state))


def main():
    initial_state = 1
    print('\nCreating two observers...')
    observer1 = ConcreteObserver('observer1')
    observer2 = ConcreteObserver('observer2')
    
    print('\nCreating subject with initial state {}...'.format(initial_state))
    subject = ConcreteSubject(initial_state)
    
    print('\nAttaching observers to subject...')
    subject.observer_attach(observer1, observer2)
    
    print('\nChanging subject state to 100...')
    subject.state = 100
    
    print('\nChanging subject state to 200...')
    subject.state = 200

if __name__ == '__main__':
    main()
