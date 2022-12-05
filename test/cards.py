from assertpy import assert_that

from texas_holdem import Card, Suite, Deck, one_pair, two_pair, search, three_of_a_kind, straight, flush, full_house, \
    straight_flush


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


def test_three_of_a_kind():
    assert_that(three_of_a_kind(Card(Suite.Spades, 3), Card(Suite.Hearts, 3), Card(Suite.Diamonds, 3))).is_true()


def test_straight():
    assert_that(straight(Card(Suite.Spades, 3), Card(Suite.Hearts, 4), Card(Suite.Diamonds, 5), Card(Suite.Clubs, 6),
                         Card(Suite.Diamonds, 7))).is_true()
    assert_that(straight(Card(Suite.Spades, 3), Card(Suite.Hearts, 10), Card(Suite.Diamonds, 5), Card(Suite.Clubs, 6),
                         Card(Suite.Diamonds, 7))).is_false()


def test_flush():
    assert_that(flush(Card(Suite.Spades, 10), Card(Suite.Spades, 12), Card(Suite.Spades, 2), Card(Suite.Spades, 7),
                      Card(Suite.Spades, 4))).is_true()

    assert_that(flush(Card(Suite.Spades, 10), Card(Suite.Spades, 12), Card(Suite.Clubs, 2), Card(Suite.Spades, 7),
                      Card(Suite.Spades, 4))).is_false()


def test_straight_flush():
    # assert_that(
    #     straight_flush(Card(Suite.Hearts, 3), Card(Suite.Hearts, 4), Card(Suite.Hearts, 5), Card(Suite.Hearts, 6),
    #                    Card(Suite.Hearts, 7))).is_true()
    assert_that(
        straight_flush(Card(Suite.Hearts, 3), Card(Suite.Hearts, 4), Card(Suite.Hearts, 5), Card(Suite.Hearts, 6),
                       Card(Suite.Diamonds, 7))).is_false()


def test_full_house():
    assert_that(
        full_house(Card(Suite.Spades, 2), Card(Suite.Hearts, 2), Card(Suite.Diamonds, 3), Card(Suite.Clubs, 3),
                   Card(Suite.Hearts, 3))).is_true()


def test_search_one_pair():
    search1 = search([Card(Suite.Spades, 2), Card(Suite.Hearts, 2)], None)
    assert_that(search1).is_equal_to('one_pair')


def test_search_two_pair():
    search1 = search([Card(Suite.Spades, 2), Card(Suite.Hearts, 2), Card(Suite.Diamonds, 3), Card(Suite.Clubs, 3)],
                     None)
    assert_that(search1).is_equal_to('two_pair')


def test_search_no_match():
    search1 = search([], [Card(Suite.Spades, 2)])
    assert_that(search1).is_equal_to(None)


def test_search():
    s = search([], [Card(Suite.Diamonds, 3), Card(Suite.Spades, 2), Card(Suite.Hearts, 2)])
    print(s)
