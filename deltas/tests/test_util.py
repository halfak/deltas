from nose.tools import eq_

from ..util import LookAhead


def test_lookahead_list():

    test_list = [1, 2, 3]

    look_ahead = LookAhead(test_list)
    eq_(look_ahead.peek(), 1)
    eq_(look_ahead.pop(), 1)
    eq_(look_ahead.peek(), 2)

    for i, val in enumerate(look_ahead):
        eq_(val, i+2)


def test_lookahead_generator():

    test_list = (i for i in [1, 2, 3])

    look_ahead = LookAhead(test_list)
    eq_(look_ahead.peek(), 1)
    eq_(look_ahead.pop(), 1)
    eq_(look_ahead.peek(), 2)

    for i, val in enumerate(look_ahead):
        eq_(val, i+2)


def test_lookahead_identity():

    l1 = LookAhead([])
    l2 = LookAhead(l1)

    eq_(l1, l2)
    eq_(id(l1), id(l2))  # Confirms same memory location
