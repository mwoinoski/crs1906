"""
Different shuffler algorithms for plug-in to card deck
using strategy design pattern. Uses template method
pattern to minimize code duplication for shuffler.
"""
from random import randint
from abc import ABCMeta, abstractmethod


class KnuthShuffler(metaclass=ABCMeta):
    """ Original Knuth shuffling algorithm. """

    def shuffle(self, deck):
        """ Randomly mix the card deck. """
        top = len(deck) - 1
        for i in range(0, top):
            swap_index = randint(self.bix(i), top)
            temp = deck[swap_index]
            deck[swap_index] = deck[i]
            deck[i] = temp

    @abstractmethod
    def bix(self, i):
        """ Force implementation in derived class. """


class SimpleKnuthShuffler(KnuthShuffler):
    """ Simple Knuth shuffler returns start index of 0. """
    def bix(self, i):
        return 0


class ModifiedKnuthShuffler(KnuthShuffler):
    """ Modified Knuth shuffler returns start index of i. """
    def bix(self, i):
        return i
