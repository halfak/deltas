from nose.tools import eq_
import pickle

from ...tokenizers import Token
from ..segments import MatchableSegment, Segment


def test_matchable_segment():

    words = ["foo", "bar", "baz"]

    ms = MatchableSegment(0, [Token(c) for c in enumerate(words)])
    eq_(ms.start, 0)
    eq_(ms.end, len(words))
    hash(ms)
    eq_(ms.match, None)
    ms.match = "derp"
    eq_(ms.match, "derp")

    d = {}
    d[ms] = ms

    ms2 = MatchableSegment(0, [Token(c) for c in enumerate(words)])
    assert ms2 in d

def test_segment():

    words = ["foo", "bar", "baz"]

    ms = Segment(0, [Token(c) for c in enumerate(words)])
    eq_(ms.start, 0)
    eq_(ms.end, len(words))

def test_equality():
    print(hash(MatchableSegment(0, [Token("zero"), Token("one")])))
    print(hash(MatchableSegment(2, [Token("zero"), Token("one")])))
    eq_(MatchableSegment(0, [Token("zero"), Token("one")]),
        MatchableSegment(2, [Token("zero"), Token("one")]))
    eq_(MatchableSegment(0, [
            MatchableSegment(0, [Token("zero"), Token("one")]),
            MatchableSegment(2, [Token("two"), Token("three")])
        ]),
        MatchableSegment(4, [
            MatchableSegment(4, [Token("zero"), Token("one")]),
            MatchableSegment(6, [Token("two"), Token("three")])
        ])
    )

def test_pickling():
    segment = MatchableSegment(0, [
        MatchableSegment(0, [Token("zero"), Token("one")]),
        Segment(2, [Token("two"), Token("three")])
    ])

    unpickled_segment = pickle.loads(pickle.dumps(segment))
    eq_(list(segment.tokens()),
        list(unpickled_segment.tokens()))
