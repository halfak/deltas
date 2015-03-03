from nose.tools import eq_

from ...tokenizers import Token
from ..segments import MatchableSegment, Segment


def test_matchable_segment():
    
    words = ["foo", "bar", "baz"]
    
    ms = MatchableSegment([Token(c, i) for i, c in enumerate(words)])
    eq_(ms.start, 0)
    eq_(ms.end, len(words))
    hash(ms)
    eq_(ms.match, None)
    ms.match = "derp"
    eq_(ms.match, "derp")
    
    d = {}
    d[ms] = ms
    
    ms2 = MatchableSegment([Token(c, i) for i, c in enumerate(words)])
    assert ms2 in d
    
def test_segment():
    
    words = ["foo", "bar", "baz"]
    
    ms = Segment([Token(c, i) for i, c in enumerate(words)])
    eq_(ms.start, 0)
    eq_(ms.end, len(words))

def test_equality():
    print(hash(MatchableSegment([Token("zero", 0), Token("one", 1)])))
    print(hash(MatchableSegment([Token("zero", 10), Token("one", 11)])))
    eq_(MatchableSegment([Token("zero", 0), Token("one", 1)]),
        MatchableSegment([Token("zero", 10), Token("one", 11)]))
    eq_(MatchableSegment([
            MatchableSegment([Token("zero", 0), Token("one", 1)]),
            MatchableSegment([Token("two", 2), Token("three", 3)])
        ]),
        MatchableSegment([
            MatchableSegment([Token("zero", 10), Token("one", 11)]),
            MatchableSegment([Token("two", 12), Token("three", 13)])
        ]),
    )
