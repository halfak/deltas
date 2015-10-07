"""
Text segmentation is the process of dividing written text into meaningful units,
such as words, sentences, or topics.  This module provides a collection of
:class:`~deltas.Segmenter` that can be used to produce hierarchical
clusters of tokens (:class:`~deltas.Segmenter`) that can be
understood by :class:`~deltas.algorithms.segment_matcher`.

:class:`~deltas.Segmenter`
    is an abstract base class that requires the implementation of a
    :func:`~deltas.Segmenter.segment`
    function that clusters tokens into a sequences of
    :class:`~deltas.Segment` and
    :class:`~deltas.MatchableSegment`

:class:`~deltas.ParagraphsSentencesAndWhitespace`
    implements a
    :func:`~deltas.ParagraphsSentencesAndWhitespace.segment`
    function that clusters tokens into segments of paragraph and
    sentence :class:`~deltas.MatchableSegment` with whitespace
    :class:`~deltas.Segment` inbetween.
"""

from .paragraphs_sentences_and_whitespace import ParagraphsSentencesAndWhitespace
from .segmenter import Segmenter
from .segments import Segment, MatchableSegment
from .functions import print_tree
