"""
Text segmentation is the process of dividing written text into meaningful units,
such as words, sentences, or topics.  This module provides a collection of
:class:`~deltas.segmenters.Segmenter` that can be used to produce hierarchical
clusters of tokens (:class:`~deltas.segmenters.Segmenter`) that can be
understood by :class:`~deltas.segment_matcher`.

:class:`~deltas.segmenters.Segmenter`
    is an abstract base class that requires the implementation of a
    :func:`~deltas.segmenters.Segmenter.segment`
    function that clusters tokens into a sequences of
    :class:`~deltas.segmenters.Segment` and
    :class:`~deltas.segmenters.MatchableSegment`

:class:`~deltas.segmenters.ParagraphsSentencesAndWhitespace`
    implements a
    :func:`~deltas.segmenters.ParagraphsSentencesAndWhitespace.segment`
    function that clusters tokens into segments of paragraph and
    sentence :class:`~deltas.segmenters.MatchableSegment` with whitespace
    :class:`~deltas.segmenters.Segment` inbetween.
"""

from .paragraphs_sentences_and_whitespace import ParagraphsSentencesAndWhitespace
from .segmenter import Segmenter
from .segments import Segment, MatchableSegment
from .functions import print_tree
