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

        subject.notify_observers()

    def test_one_observer(self):
        subject = SimpleSubject()
        observer1 = Mock(Observer)
        subject.add_observer(observer1)
        subject.add_observer(observer1)

        subject.notify_observers()

        observer1.notify.assert_called_once_with(subject)

    def test_two_observers(self):
        subject = SimpleSubject()
        observer1 = Mock(Observer)
        subject.add_observer(observer1)
        observer2 = Mock(Observer)
        subject.add_observer(observer2)

        subject.notify_observers()

        observer1.notify.assert_called_once_with(subject)
        observer2.notify.assert_called_once_with(subject)
