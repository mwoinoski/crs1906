"""
observer.py - Example of Observer design pattern.
"""

from abc import ABC, abstractmethod
import itertools


class Subject(ABC):
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


class Observer(ABC):
    @abstractmethod
    def update(self, subject):
        """ Subject notifies observer by calling this method """


class ConcreteSubject(Subject):
    def __init__(self, value=None):
        super().__init__()
        self._state = value

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
        print(f'{self._name}.update() called, subject state = {subject.state}')


def main():
    initial_state = 1
    print(f'\nCreating subject with initial state {initial_state}...')
    subject = ConcreteSubject(initial_state)
    
    print('\nCreating two observers...')
    observer1 = ConcreteObserver('observer1')
    observer2 = ConcreteObserver('observer2')
    
    print('\nAttaching observers to subject...')
    subject.observer_attach(observer1, observer2)
    
    print('\nChanging subject state to 100...')
    subject.state = 100
    
    print('\nChanging subject state to 200...')
    subject.state = 200

if __name__ == '__main__':
    main()
