"""
The primary use-case of this library is to detect differences between two
sequences of tokens.  So far, two such detectors are available:

:class:`~deltas.detection.sequence_matcher`
    implementes :func:`~deltas.detection.sequence_matcher.diff` that wraps
    :class:`difflib.SequenceMatcher`
:class:`~deltas.detection.segment_matcher`
    implementes :func:`~deltas.detection.segment_matcher.diff` that
    uses a :class:`~deltas.segmenters.Segmenter` to detect block moves

:Example:

    >>> from deltas import segment_matcher, apply
    >>> from deltas.tokenizers import text_split
    >>>
    >>> a_text = "This comes first. This comes second."
    >>> b_text = "This comes second. This comes first."
    >>> a, b = list(text_split.tokenize(a_text)), list(text_split.tokenize(b_text))
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
from .detector import Detector
from .segment_matcher import SegmentMatcher
from .sequence_matcher import SequenceMatcher
