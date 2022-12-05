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

    def __lt__(self, other):
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
    final = {Card.parse(word) for word in words}
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

order = ['high_card', 'one_pair', 'two_pair', 'three_of_a_kind', 'straight', 'flush', 'full_house', 'four_of_a_kind',
         'straight_flush', 'royal_flush'
         ]


def search(deck):
    results = set()
    search_([], [*deck], results)
    results = [*results]
    results.sort()
    if results:
        return results[-1]
    else:
        return Result('high_card', [], [*deck])


def process(*lines):
    results = dict()

    print("")
    p = {line: search(parse_line(line)) for line in lines}
    r = [*p.values()]
    r.sort()
    results = [f'{k} {v.hand}{" winner" if v == r[-1] else ""}' for k, v in p.items()]
    # results = [k for k, v in p.items()]
    for r in results:
        print(r)
    return results


@total_ordering
class Result:
    hand = None
    cards = set()
    deck = []

    def __init__(self, hand, cards, deck):
        self.hand = hand
        self.cards = {*cards}
        self.deck = deck.copy()
        self.deck.sort()

    def __eq__(self, other: object) -> bool:
        return self.hand == other.hand and self.cards == other.cards and self.deck == other.deck

    def __repr__(self):
        return self.hand + ' ' + str(self.cards) + ' ' + str(self.deck)

    def __hash__(self):
        return hash((self.hand, tuple(self.cards), tuple(self.deck)))

    def __lt__(self, other):
        if self.index == other.index:
            if self.deck and not other.deck:
                return False
            elif not self.deck and other.deck:
                return True
            elif not self.deck and not other.deck:
                return False
            else:
                return self.deck[-1] < other.deck[-1]
        else:
            return self.index < other.index

    @property
    def index(self):
        return order.index(self.hand)


def can_add(r, results):
    if not results:
        return True
    else:
        newlist = [x for x in results if x.index < r.index]
        return len(newlist) > 0


def search_(cards, deck, results):
    match = [m.__name__ for m in matches if m(*cards)]
    match = match[0] if len(match) > 0 else None
    if match:
        r = Result(match, cards, deck)
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
