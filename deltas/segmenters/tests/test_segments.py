from nose.tools import eq_

from ..segments import Token, IndexedSegment, MatchableSegment, \
                       TokenSequence, MatchableTokenSequence, \
                       SegmentNodeCollection, MatchableSegmentNodeCollection

def test_matchable_types():
    
    tokens = ["foo", " ", "bar", " ", "baz"]
    
    ms = MatchableSegment(b"checksum test", match="derp")
    hash(ms)
    eq_(ms.match, "derp")
    
    t = Token(0, tokens[0])
    hash(t)
    
    mts = MatchableTokenSequence([Token(i, c) for i, c in enumerate(tokens)])
    hash(mts)
    
    msnc = MatchableSegmentNodeCollection(
            [MatchableTokenSequence([Token(i, c) for i, c in enumerate(tokens)])])
    hash(msnc)

def test_indexable_types():
    tokens = ["foo", " ", "bar", " ", "baz"]
    
    iis = IndexedSegment(0, 1)
    eq_(iis.start, 0)
    eq_(iis.end, 1)
    eq_(len(iis), 1)
    
    t = Token(0, tokens[0])
    eq_(t.start, 0)
    eq_(t.end, 1)
    eq_(len(t), 1)
    
    ts = TokenSequence([Token(i, c) for i, c in enumerate(tokens)])
    eq_(ts.start, 0)
    eq_(ts.end, len(tokens))
    
    snc = SegmentNodeCollection(
            [TokenSequence([Token(i, c) for i, c in enumerate(tokens)])])
    eq_(snc.start, 0)
    eq_(snc.end, len(tokens))

def test_equality():
    t1 = Token(0, "foo")
    t2 = Token(1, "foo")
    eq_(hash(t1), hash(t2))
    eq_(t1, t2)
