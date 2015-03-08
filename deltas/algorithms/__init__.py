"""
The primary use-case of this library is to detect differences between two
sequences of tokens.  So far, two such algorithmic strategies are available:

:class:`~deltas.algorithms.sequence_matcher`
    implementes :func:`~deltas.algorithms.sequence_matcher.diff` that will
    compare two sequences of :class:`~deltas.tokenizers.Token` and return
    a set of operations.
:class:`~deltas.algorithms.segment_matcher`
    implementes :func:`~deltas.algorithms.segment_matcher.diff` that
    uses a :class:`deltas.segmenters.Segmenter` to detect block moves

Both of these algorithms are supplimented with an
:class:`delta.algorithms.Engine` and `process()` for more efficiently
processing several revisions of the same text

:Example:

    >>> from deltas import segment_matcher, apply
    >>> from deltas.tokenizers import text_split
    >>>
    >>> a = text_split.tokenize("This comes first. This comes second.")
    >>> b = text_split.tokenize("This comes second. This comes first.")
    >>>
    >>> operations = segment_matcher.diff(a, b)
    >>>
    >>> for op in operations:
    ...     print("{0}: '{1}'".format(op.name, "".join(op.relevant_tokens(a, b))))
    ...
    equal: 'This comes second.'
    insert: ' '
    equal: 'This comes first.'
    delete: ' '
"""
from .engine import Engine
from .segment_matcher import SegmentMatcher
from .sequence_matcher import SequenceMatcher
