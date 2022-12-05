from assertpy import assert_that

from texas_holdem import Card, Suite, one_pair, two_pair, search, three_of_a_kind, straight, flush, full_house, \
    straight_flush, royal_flush, four_of_a_kind, parse_line, process


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
    assert_that(
        straight_flush(Card(Suite.Hearts, 3), Card(Suite.Hearts, 4), Card(Suite.Hearts, 5), Card(Suite.Hearts, 6),
                       Card(Suite.Hearts, 7))).is_true()

    assert_that(
        straight_flush(Card(Suite.Hearts, 3), Card(Suite.Hearts, 4), Card(Suite.Hearts, 5), Card(Suite.Hearts, 6),
                       Card(Suite.Diamonds, 7))).is_false()


def test_royal_flush():
    assert_that(
        royal_flush(Card(Suite.Hearts, 10), Card(Suite.Hearts, 11), Card(Suite.Hearts, 12), Card(Suite.Hearts, 13),
                    Card(Suite.Hearts, 14))).is_true()


def test_full_house():
    assert_that(
        full_house(Card(Suite.Spades, 2), Card(Suite.Hearts, 2), Card(Suite.Diamonds, 3), Card(Suite.Clubs, 3),
                   Card(Suite.Hearts, 3))).is_true()


def test_four_of_a_kind():
    assert_that(
        four_of_a_kind(Card(Suite.Spades, 2), Card(Suite.Hearts, 2), Card(Suite.Diamonds, 2),
                       Card(Suite.Clubs, 2))).is_true()
    assert_that(
        four_of_a_kind(Card(Suite.Spades, 2), Card(Suite.Hearts, 3), Card(Suite.Diamonds, 2),
                       Card(Suite.Clubs, 2))).is_false()


def test_search_one_pair():
    search1 = search([Card(Suite.Spades, 2), Card(Suite.Hearts, 2)])
    assert_that(search1.hand).is_equal_to('one_pair')


def test_search_two_pair():
    search1 = search([Card(Suite.Spades, 2), Card(Suite.Hearts, 2), Card(Suite.Diamonds, 3), Card(Suite.Clubs, 3)]
                     )
    assert_that(search1.hand).is_equal_to('two_pair')


def test_search_no_match():
    search1 = search([Card(Suite.Spades, 2)])
    assert_that(search1.hand).is_equal_to('high_card')


def test_search():
    s = search([], [Card(Suite.Diamonds, 3), Card(Suite.Spades, 2), Card(Suite.Hearts, 2)])
    print(s)


def test_search():
    s = search([Card(Suite.Diamonds, 3), Card(Suite.Spades, 2), Card(Suite.Hearts, 2), Card(Suite.Clubs, 10),
                Card(Suite.Clubs, 2)])
    assert_that(s.hand).is_equal_to('three_of_a_kind')


def test_parse_card():
    assert_that(Card.parse('Kc')).is_equal_to(Card(Suite.Clubs, 13))
    assert_that(Card.parse('Ts')).is_equal_to(Card(Suite.Spades, 10))


def test_parse_line():
    assert_that(parse_line('Kc 9s Ks Kd 9d 3c 6d')).contains_only(Card(Suite.Clubs, 13),
                                                                  Card(Suite.Spades, 9), Card(Suite.Spades, 13),
                                                                  Card(Suite.Diamonds, 13),
                                                                  Card(Suite.Diamonds, 9), Card(Suite.Clubs, 3),
                                                                  Card(Suite.Diamonds, 6))


def test_search_1():
    s = search(parse_line('Kc 9s Ks Kd 9d 3c 6d'))
    assert_that(s.hand).is_equal_to('full_house')
    s = search(parse_line('9c Ah Ks Kd 9d 3c 6d'))
    assert_that(s.hand).is_equal_to('two_pair')
    s = search(parse_line('4d 2d Ks Kd 9d 3c 6d'))
    assert_that(s.hand).is_equal_to('flush')


def test_process():
    print("")
    l = process('9c Ah Ks Kd 9d 3c 6d', '4d 2d Ks Kd 9d 3c 6d', '4d Ks Jh', 'Kc 9s Ks Kd 9d 3c 6d')
    assert_that(l).contains_only('9c Ah Ks Kd 9d 3c 6d two_pair', '4d 2d Ks Kd 9d 3c 6d flush', '4d Ks Jh high_card',
                                 'Kc 9s Ks Kd 9d 3c 6d full_house winner')


def test_search_with_high_card_decider():
    process('3c 3s Kd Js', '3c 3h Th 9h')
