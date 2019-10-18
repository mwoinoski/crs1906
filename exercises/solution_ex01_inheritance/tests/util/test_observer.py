"""
Unit tests for Observer and Subject classes
"""

__author__ = 'Mike Woinoski (mike@articulatedesign.us.com)'

from unittest import TestCase
from unittest.mock import Mock

from ticketmanor.util.observer import Subject, Observer

class SimpleSubject(Subject):
    pass


class ObserverTest(TestCase):
    """Unit tests for Observer"""

    def test_no_observers(self):
        subject = SimpleSubject()

        subject.observer_notify()

    def test_one_observer(self):
        subject = SimpleSubject()
        observer1 = Mock(Observer)
        subject.observer_attach(observer1)
        subject.observer_attach(observer1)

        subject.observer_notify()

        observer1.update.assert_called_with(subject)

    def test_two_observers(self):
        subject = SimpleSubject()
        observer1 = Mock(Observer)
        subject.observer_attach(observer1)
        observer2 = Mock(Observer)
        subject.observer_attach(observer2)

        subject.observer_notify()

        observer1.update.assert_called_with(subject)
        observer2.update.assert_called_with(subject)
