from enum import Enum


class Suite(Enum):
    Spades = 1
    Hearts = 2
    Diamonds = 3
    Clubs = 4


class Card:
    suite = None
    value = -1

    def __init__(self, suite, value):
        self.suite = suite
        self.value = value


class Deck:
    cards = {}

    def __init__(self, *args):
        self.cards = {*args}

    def get_min(self):
        highest = None
        for card in self.cards:
            if not highest or card.value < highest.value:
                highest = card
        return highest


def one_pair(*cards):
    number = None
    count = 0
    if len(cards) != 2:
        return False

    for c in cards:
        if not number:
            number = c.value
            count = count + 1
        elif number == c.value:
            count = count + 1
    return count == 2
