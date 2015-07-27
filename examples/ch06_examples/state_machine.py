"""
state_machine.py - Example of a State Machine implementation
from Chapter 6
"""

import os
import logging
import logging.config

log_conf = 'logging.conf'
logging.config.fileConfig(os.path.dirname(__file__) + '/' + log_conf)
logger = logging.getLogger(__name__)


class State:
    """An individual state of a state machine"""

    def __init__(self, name, *, transitions=None,
                 enter_action=None, exit_action=None):
        """
        Initialize the State

        :param name: Name of state
        :param transitions: list of Transition
        :param enter_action: function to executed when state is entered
        :param exit_action: function to executed when state exiting state
        """
        self.name = name
        self.enter_action = enter_action
        self.exit_action = exit_action
        self.transitions = None
        if transitions:
            if len(set(transitions)) != len(transitions):
                raise ValueError('Transition events in a state must be unique')
            self.transitions = {t.event: t for t in transitions}

    def add_transition(self, transition):
        """Add Transition to collection of transitions"""
        self.transitions[transition.event] = transition

    def __repr__(self):
        return self._marshal(repr, self.enter_action, self.exit_action)

    def __str__(self):
        return self._marshal(
            str,
            self.enter_action.__name__ if self.enter_action else None,
            self.exit_action.__name__ if self.exit_action else None)

    def _marshal(self, display_func, enter_value, exit_value):
        trans_str = \
            ",".join(display_func(t) for t in self.transitions.values()) \
            if self.transitions else ''
        return "(name={},enter_action={},exit_action={},transitions=[{}])" \
            .format(self.name, enter_value, exit_value, trans_str)


class Transition:
    """Models a transition between states"""

    def __init__(self, *, event, target, guard=None, action=None):
        """
        Initialize the Transition.

        :param event: event that triggers the transition.
        :param target: function that returns a reference to the target State.
            This is a function rather than a reference to a State so a
            Transition can have a target State that is defined later in
            the source file.
        :param guard: boolean function. The transition is triggered iff
            the guard function returns true
        :param action: function called when transition is triggered.
        """
        self.event = event
        self.target = target
        self.guard = guard
        self.action = action

    def __repr__(self):
        return '(event={},target={},guard={},action={})'\
            .format(self.event, self.target, self.guard, self.action)

    def __str__(self):
        return '(event={},target={},guard={},action={})'\
            .format(self.event,
                    self.target().name if self.target else None,
                    self.guard.__name__ if self.guard else None,
                    self.action.__name__ if self.action else None)


class StateMachine:
    """Models a State Machine"""

    def __init__(self, states):
        """Initialize the StateMachine

        :param states: list of State instances
        """
        self.states = states
        self.current_state = states[0]
        self.history = []  # for unit testing

    def handle_event(self, event):
        """
        Handle an event. This may cause a state transition.

        :param event: The triggering event. Events are used as keys to lookup
            the associated Transition for the current State. If there is no
            match for an event in the State's collection of Transitions, the
            event is ignored.
        """
        if self.current_state.transitions:  # else machine is at its end state
            transition = self.current_state.transitions.get(event, None)
            self._handle_transition(transition, event)

    def _handle_transition(self, transition, event):
        if transition and \
                (transition.guard is None or transition.guard(event)):
            # execute exit action for old state
            if self.current_state.exit_action:
                self.current_state.exit_action(event)
            logger.debug(
                "%s state got event %s, transitioning to %s",
                self.current_state.name, event, transition.target().name)
            # execute action for transition
            if transition.action:
                transition.action(event)
            # change to new state
            self.current_state = transition.target()
            self.history.append(self.current_state)
            # execute enter action for new state
            if self.current_state.enter_action:
                self.current_state.enter_action(event)
            # check if current state auto-transitions to a new state
            if self.current_state.transitions:
                for trans in self.current_state.transitions.values():
                    # if transition does not have an event, it happens automatically
                    if not trans.event:
                        # we found an auto transition
                        self._handle_transition(trans, event)
                        break

    def start(self, *args):
        """Start the state machine"""
        self.history.append(self.current_state)
        if self.current_state.enter_action:
            self.current_state.enter_action(*args)

    def __repr__(self):
        return 'states={},current_state={}'\
            .format(",".join(str(s) for s in self.states), self.current_state)

    def __str__(self):
        return self.__repr__()
