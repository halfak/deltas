"""
Segments represent subsequences of tokens that have interesting properties.  All
segments are based on two abstract types:

:class:`deltas.Segment`
    A segment of text with a ``start`` and ``end`` index that refers to the
    original sequence of tokens.
:class:`deltas.MatchableSegment`
    A segment of text that can be matched with another segment no matter where
    it appears in a document.  Generally segmnents of this type represent a
    substantial collection of tokens.

Segment Types
^^^^^^^^^^^^^

.. autoclass:: deltas.Segment
    :members:

.. autoclass:: deltas.MatchableSegment
    :members:
"""
import hashlib


class Segment(list):
    __slots__ = ("start", )
    """
    Represents a sequence of of tokens.  Note that plain Segments are not
    matchable.  Plain segments are generally reserved for whitespace.  For
    matchable segments, see :class:`~deltas.MatchableSegment`.

    Note that :class:`~deltas.Segment` behaves like a list, but it
    will expect that everything added will be of type
    :class:`~deltas.Segment` or :class:`~deltas.Token`.
    """
    def __new__(cls, *args, **kwargs):
        if len(args) == 1 and len(kwargs) == 0 and isinstance(args[0], cls):
            args[0]
        else:
            inst = super().__new__(cls, *args, **kwargs)
            inst.initialize(*args, **kwargs)
            return inst

    def __init__(self, *args, **kwargs): pass

    def initialize(self, start=0, subsegments=None):
        subsegments = subsegments or []
        super().__init__(subsegments)
        self.start = int(start)

    def tokens(self):
        """
        `generator` : the tokens in this segment
        """
        for subsegment_or_token in self:
            if isinstance(subsegment_or_token, Segment):
                subsegment = subsegment_or_token
                for token in subsegment.tokens():
                    yield token
            else:
                token = subsegment_or_token
                yield token

    @property
    def end(self):
        """
        The index of the last :class:`deltas.Token` in the segment.
        """
        return self.start + sum(1 for _ in self.tokens())

    def __repr__(self):
        return "{0}({1})".format(self.__class__.__name__, super().__repr__())

    def __str__(self):
        return ''.join(str(ss) for ss in self)

    def __eq__(self, other):
        raise NotImplementedError()

    def __neq__(self, other):
        raise NotImplementedError()

    def __hash__(self, other):
        raise NotImplementedError()


class MatchableSegment(Segment):
    """
    Constructs a segment that can be matched.  Segments of this type general
    contain important content that might have been copied between different
    versions of text.
    """
    __slots__ = ("sha1", "match")

    def initialize(self, *args, **kwargs):
        super().initialize(*args, **kwargs)
        self.sha1 = hashlib.sha1(bytes(str(self), 'utf-8'))
        self.match = None

    def __eq__(self, other):
        try:
            return hash(self) == hash(other)
        except AttributeError:
            return False

    def __neq__(self, other):
        try:
            return hash(self) != hash(other)
        except AttributeError:
            return False

    def __hash__(self):
        return hash(self.sha1.digest())

    def __getstate__(self): return (self.start, list(self))
    def __setstate__(self, args): self.initialize(*args)

    def append(self, subsegment):
        super().append(subsegment)
        self.sha1.update(bytes(str(subsegment), 'utf-8'))

    def extend(self, subsegments):
        for subsegment in subsegments:
            self.append(subsegment)
