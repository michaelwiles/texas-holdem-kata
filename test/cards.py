from assertpy import assert_that

from texas_holdem import Card, Suite, Deck, one_pair, two_pair


def test_lowest():
    card1 = Card(Suite.Spades, 2)
    card2 = Card(Suite.Spades, 1)
    d = Deck(card1, card2)
    assert_that(d.get_min().value).is_equal_to(1)


def test_one_pair():
    assert_that(one_pair(Card(Suite.Spades, 2), Card(Suite.Hearts, 2))).is_true()

def test_two_pair():
    assert_that(
        two_pair(Card(Suite.Spades, 2), Card(Suite.Hearts, 2), Card(Suite.Diamonds, 3), Card(Suite.Clubs, 3))).is_true()
    assert_that(two_pair(Card(Suite.Spades, 2), Card(Suite.Hearts, 2), Card(Suite.Diamonds, 3),
                         Card(Suite.Clubs, 5))).is_false()
