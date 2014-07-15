"""
Segments represent subsequences of tokens that have interesting properties.  All
segments are based on two abstract types:

:class:`deltas.segmenters.segments.IndexedSegment`
    A segment of text with a ``start`` and ``end`` index that refers to the
    original sequence of tokens.
:class:`deltas.segmenters.segments.MatchableSegment`
    A segment of text that can be matched with another segment no matter where
    it appears in a document.  Generally segmnents of this type represent a
    substantial collection of tokens.

Segment Types
^^^^^^^^^^^^^

.. autoclass:: deltas.segmenters.segments.IndexedSegment
    :members:

.. autoclass:: deltas.segmenters.segments.MatchableSegment
    :members:

.. autoclass:: deltas.segmenters.segments.Token
    :members:

.. autoclass:: deltas.segmenters.segments.SegmentNode
    :members:

.. autoclass:: deltas.segmenters.segments.MatchableSegmentNode
    :members:

.. autoclass:: deltas.segmenters.segments.TokenSequence
    :members:

.. autoclass:: deltas.segmenters.segments.MatchableTokenSequence
    :members:

.. autoclass:: deltas.segmenters.segments.SegmentNodeCollection
    :members:

.. autoclass:: deltas.segmenters.segments.MatchableSegmentNodeCollection
    :members:
"""
import types
from hashlib import sha1
from itertools import chain

from ..util import LookAhead


def generate_checksum(string):
    string = str(string)
    return sha1(bytes(string, 'utf-8', 'replace')).digest()

class IndexedSegment:
    """
    A segment of text with a ``start`` and ``end`` index that refers to the
    original sequence of tokens.
    """
    def __init__(self, start, end):
        self.start = int(start)
        self.end = int(end)
    
    def __len__(self):
        return self.end - self.start

class MatchableSegment:
    """
    A segment of text that can be matched with another segment no matter where
    it appears in a document.  Generally segmnents of this type represent a
    substantial collection of tokens.
    """
    def __init__(self, checksum, match=None):
        self.checksum = bytes(checksum)
        self.match = match
    
    def __hash__(self):
        return hash(self.checksum)
    
    def __eq__(self, other):
        try:
            return hash(self) == hash(other)
        except TypeError:
            raise TypeError("Cannot compare {0} ".format(type(self)) + \
                            "to {0}.".format(type(other)))
    
    def __neq__(self, other):
        return not self == other
    
    


class Token(MatchableSegment, IndexedSegment):
    """
    A token of content.  Both indexed and matchable
    
    :Parameters:
        start : int
            The index at which the token appears in the original token sequence.
        content : `str`
            The content of the token.
        
    """
    def __new__(cls, *args):
        if len(args) == 1:
            if isinstance(args[0], cls):
                return args[0]
            else:
                raise TypeError("Expected {0}, got {1}".format(cls,
                                                               type(args[0])))
                
        elif len(args) == 2:
            start, content = args
            inst = super().__new__(cls)
            inst.initiate(start, content)
            return inst
        
        else:
            raise TypeError("Expected 2 arguments, " + \
                            "got {0}:{1}".format(len(args), repr(args)))
    
    def __init__(self, *args, **kwargs): pass
    
    def initiate(self, start, content):
        IndexedSegment.__init__(self, start, start+1)
        MatchableSegment.__init__(self, generate_checksum(content))
        
        self.content = str(content)
    
    def __str__(self): return self.content
    
    def __repr__(self):
        return repr(self.content)
    
    def tokens(self): yield self

class SegmentNode(IndexedSegment, list):
    """
    An indexed list of :class:`~deltas.segmenters.segments.IndexedSegment`.
    
    :Parameters:
        children : :class:`~deltas.segmenters.segments.IndexedSegment`.
            All segment node children
    
    """
    def __init__(self, children):
        list.__init__(self, children)
        IndexedSegment.__init__(self, self[0].start, self[-1].end)
    
    def tokens(self): raise NotImplementedError()
    
    def __repr__(self):
        return "{0}({1})".format(self.__class__.__name__, list.__repr__(self))


class MatchableSegmentNode(MatchableSegment, SegmentNode):
    """
    A matchable indexed list of :class:`~deltas.segmenters.segments.SegmentNode`.
    
    :Parameters:
        children : :class:`~deltas.segmenters.segments.SegmentNode`.
            All segment node children
    
    """
    def __init__(self, children, match=None):
        SegmentNode.__init__(self, children)
        checksum = generate_checksum("".join(str(t)
                                     for child in children
                                     for t in child.tokens()))
        
        MatchableSegment.__init__(self, checksum, match=match)

class TokenSequence(SegmentNode):
    """
    An list of :class:`~deltas.segmenters.segments.Token`.
    
    :Parameters:
        tokens : :class:`~deltas.segmenters.segments.Token`.
            All token children
    
    """
    def __init__(self, tokens):
        SegmentNode.__init__(self, tokens)
        
    def tokens(self): return self


class MatchableTokenSequence(MatchableSegment, TokenSequence):
    """
    A matchable list of :class:`~deltas.segmenters.segments.Token`.
    
    :Parameters:
        tokens : :class:`~deltas.segmenters.segments.Token`.
            All token children
    
    """
    def __init__(self, tokens, match=None):
        TokenSequence.__init__(self, tokens)
        hash = sha1(b"".join(bytes(t.content, 'utf-8') for t in tokens))
        
        MatchableSegment.__init__(self, hash.digest(), match=match)
    

class SegmentNodeCollection(SegmentNode, list):
    """
    A list of :class:`~deltas.segmenters.segments.SegmentNode`.
    
    :Parameters:
        tokens : :class:`~deltas.segmenters.segments.SegmentNode`.
            All node children
    
    """
    def __init__(self, children):
        assert sum(isinstance(c, SegmentNode) for c in children) == len(children)
        SegmentNode.__init__(self, children)
        list.__init__(self, children)
    
    def tokens(self): return (t for c in children for t in c.tokens())
    

class MatchableSegmentNodeCollection(SegmentNodeCollection,
                                     MatchableSegmentNode):
    """
    A matchable list of :class:`~deltas.segmenters.segments.SegmentNode`.

    :Parameters:
     tokens : :class:`~deltas.segmenters.segments.SegmentNode`.
         All node children

    """
    def __init__(self, children, match=None):
        SegmentNodeCollection.__init__(self, children)
        MatchableSegmentNode.__init__(self, children, match=match)
