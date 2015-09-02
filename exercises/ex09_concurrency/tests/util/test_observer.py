"""
Unit tests for Observer and Observable classes
"""

from unittest import TestCase
from unittest.mock import Mock, call

from ticketmanor.util.observer import Subject, Observer

__author__ = 'Mike Woinoski (mike@articulatedesign.us.com)'


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
        subject.observer_attach(observer1)  # Observer.update() called here

        subject.observer_notify()  # Observer.update() called here again

        observer1.update.assert_has_calls([call(subject), call(subject)])

    def test_two_observers(self):
        subject = SimpleSubject()
        observer1 = Mock(Observer)
        subject.observer_attach(observer1)
        observer2 = Mock(Observer)
        subject.observer_attach(observer2)

        subject.observer_notify()

        # Observer.update() called at Subject.observer_attach() and
        # Subject.observer_notify()
        observer1.update.assert_has_calls([call(subject), call(subject)])
        observer2.update.assert_has_calls([call(subject), call(subject)])
