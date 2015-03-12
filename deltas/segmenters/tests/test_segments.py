from nose.tools import eq_

from ...tokenizers import Token
from ..segments import MatchableSegment, Segment


def test_matchable_segment():

    words = ["foo", "bar", "baz"]

    ms = MatchableSegment([Token.construct(c, i) for i, c in enumerate(words)])
    eq_(ms.start, 0)
    eq_(ms.end, len(words))
    hash(ms)
    eq_(ms.match, None)
    ms.match = "derp"
    eq_(ms.match, "derp")

    d = {}
    d[ms] = ms

    ms2 = MatchableSegment([Token.construct(c, i) for i, c in enumerate(words)])
    assert ms2 in d

def test_segment():

    words = ["foo", "bar", "baz"]

    ms = Segment([Token.construct(c, i) for i, c in enumerate(words)])
    eq_(ms.start, 0)
    eq_(ms.end, len(words))

def test_equality():
    eq_(MatchableSegment([Token.construct("zero", 0), Token.construct("one", 1)]),
        MatchableSegment([Token.construct("zero", 2), Token.construct("one", 4)]))
    eq_(MatchableSegment([
            MatchableSegment([Token.construct("zero", 0), Token.construct("one", 1)]),
            MatchableSegment([Token.construct("two", 2), Token.construct("three", 4)])
        ]),
        MatchableSegment([
            MatchableSegment([Token.construct("zero", 0), Token.construct("one", 1)]),
            MatchableSegment([Token.construct("two", 2), Token.construct("three", 3)])
        ]),
    )
