import string

from functools import total_ordering

from enum import Enum


class Suite(Enum):
    Spades = 'Spades'
    Hearts = 'Hearts'
    Diamonds = 'Diamonds'
    Clubs = 'Clubs'


lookup = {Suite.Spades: 1, Suite.Hearts: 2, Suite.Diamonds: 3, Suite.Clubs: 4}

values = ['X', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
suites = {'c': Suite.Clubs, 's': Suite.Spades, 'd': Suite.Diamonds, 'h': Suite.Hearts}


@total_ordering
class Card:
    suite = None
    value = -1

    def __init__(self, suite, value):
        self.suite = suite
        self.value = value

    def __le__(self, other):
        if self.value != other.value:
            return self.value < other.value
        self_suite = lookup[self.suite]
        other_suite = lookup[other.suite]
        return self_suite < other_suite

    def __eq__(self, other):
        return self.value == other.value and self.suite == other.suite

    def __hash__(self):
        x = 0
        if self.value:
            x += self.value * 10
        if self.suite:
            x += self.suite.__hash__()
        return x

    def __repr__(self):
        return str(self.value) + ':' + str(self.suite)

    @staticmethod
    def parse(card_string: string):
        value = card_string[0]
        value = values.index(value)
        suite = suites[card_string[1]]
        c = Card(suite, value)
        return c


def parse_line(line):
    words = line.split()
    final = [Card.parse(word) for word in words]
    return final


def one_pair(*cards):
    return find_duplicates(2, *cards)


def find_duplicates(number_of_duplicate, *cards):
    number = None
    count = 0
    if len(cards) != number_of_duplicate:
        return False

    for c in cards:
        if not number:
            number = c.value
            count = count + 1
        elif number == c.value:
            count = count + 1
    return count == number_of_duplicate


def four_of_a_kind(*cards):
    return find_duplicates(4, *cards)


def three_of_a_kind(*cards):
    return find_duplicates(3, *cards)


def flush(*cards):
    suite = None
    if len(cards) != 5:
        return False
    for card in cards:
        if suite and card.suite != suite:
            return False
        suite = card.suite
    return True


def straight(*cards):
    cards = [*cards]
    cards.sort()
    index = 0
    found = None
    if len(cards) != 5:
        return False
    for card in cards:
        if not found:
            found = card
            index = index + 1
        elif found.value + 1 != card.value:
            return False
        index = index + 1
        found = card
    return True


def royal_flush(*cards):
    cards = [*cards]
    cards.sort()
    if len(cards) != 5:
        return False
    elif cards[0].value != 10:
        return False
    else:
        return straight_flush(*cards)


def straight_flush(*cards):
    cards = [*cards]
    cards.sort()
    index = 0
    found = None
    if len(cards) != 5:
        return False
    for card in cards:
        if not found:
            found = card
            index = index + 1
        elif found.value + 1 != card.value or found.suite != card.suite:
            return False
        index = index + 1
        found = card
    return True


def full_house(*cards):
    if len(cards) != 5:
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

    # return len(sets[keys[0]]) == 2 and len(sets[keys[1]]) == 2
    totals = {len(i) for i in sets.values()}
    return 2 in totals and 3 in totals


def two_pair(*cards):
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


matches = [
    royal_flush, straight_flush, four_of_a_kind, full_house, flush, straight, three_of_a_kind, two_pair, one_pair]

order = ['royal_flush', 'straight_flush', 'four_of_a_kind', 'full_house', 'flush', 'straight', 'three_of_a_kind',
         'two_pair', 'one_pair']


def search(cards, deck):
    results = set()
    search_(cards, deck, results)
    return results


class Result:
    hand = None
    cards = set()

    def __init__(self, hand, cards):
        self.hand = hand
        self.cards = {*cards}

    def __eq__(self, other: object) -> bool:
        return self.hand == other.hand and self.cards == other.cards

    def __repr__(self):
        return self.hand + ' ' + str(self.cards)

    def __hash__(self):
        x = 1
        if self.hand:
            x += self.hand.__hash__()
        if not self.cards:
            x += self.cards.__hash__()
        return x

    @property
    def index(self):
        return order.index(self.hand)


def can_add(r, results):
    if not results:
        return True
    else:
        newlist = [x for x in results if x.index > r.index]
        return len(newlist) > 0


def search_(cards, deck, results):
    match = [m.__name__ for m in matches if m(*cards)]
    match = match[0] if len(match) > 0 else None
    if match:
        r = Result(match, cards)
        if can_add(r, results):
            results.add(r)
    for i in range(len(deck)):
        new_card = deck[i]
        new_cards = cards.copy()
        new_cards.append(new_card)
        new_deck = deck.copy()
        new_deck.pop(i)
        search_(new_cards, new_deck, results)
    return results
