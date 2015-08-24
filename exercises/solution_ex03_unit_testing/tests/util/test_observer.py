"""
Unit tests for Observer and Observable classes
"""

__author__ = 'Mike Woinoski (michaelw@articulatedesign.us.com)'

from unittest import TestCase
from unittest.mock import Mock

from ticketmanor.util.observer import Observable, Observer

class SimpleObservable(Observable):
    pass


class ObserverTest(TestCase):
    """Unit tests for Observer"""

    def test_no_observers(self):
        observable = SimpleObservable()

        observable.notify_observers()

    def test_one_observer(self):
        observable = SimpleObservable()
        observer1 = Mock(Observer)
        observable.add_observer(observer1)
        observable.add_observer(observer1)

        observable.notify_observers()

        observer1.notify.assert_called_once_with(observable)

    def test_two_observers(self):
        observable = SimpleObservable()
        observer1 = Mock(Observer)
        observable.add_observer(observer1)
        observer2 = Mock(Observer)
        observable.add_observer(observer2)

        observable.notify_observers()

        observer1.notify.assert_called_once_with(observable)
        observer2.notify.assert_called_once_with(observable)
