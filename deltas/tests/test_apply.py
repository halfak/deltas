from nose.tools import eq_

from ..apply import apply
from ...types import Insert, Persist, Remove


def test_apply():
    a = [0,1,2,3,4,5,6]
    b = [0,1,2,3,"four", "five", "six", "seven", "eight", "nine", 6]
    replayed_b = list(apply([Insert(0, 4, b[0:4]), Remove(4, 6, a[4:6]),
                             Insert(4, 10, b[4:10]), Persist(6, 7)],
                             a))
    eq_(b, replayed_b)
