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


def two_pair(*cards):
    first_pair = {}
    second_pair = {}
    first_number = -1
    second_number = -1
    if len(cards) != 4:
        return False

    sets = dict()
    for c in cards:
        if c.value not in sets:
            sets[c.value] = [c]
        else:
            sets[c.value].append(c)
    keys = [*sets.keys()]
    if len(sets) != 2:
        return False
    return len(sets[keys[0]]) == 2 and len(sets[keys[1]]) == 2


matches = [one_pair, two_pair]


def search(cards, deck):
    return next(m.__name__ for m in matches if m(*cards))
