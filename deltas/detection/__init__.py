"""
The primary use-case of this library is to detect differences between two
sequences of tokens.  So far, two such detectors are available:

:class:`~deltas.detection.sequence_matcher`
    implementes :func:`~deltas.detection.sequence_matcher.diff` that wraps
    :class:`difflib.SequenceMatcher`
:class:`~deltas.detection.segment_matcher`
    implementes :func:`~deltas.detection.segment_matcher.diff` that
    uses a :class:`~deltas.segmenters.Segmenter` to detect block moves
"""
