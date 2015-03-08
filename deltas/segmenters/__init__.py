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

:class:`~deltas.ParagraphsSentencesAndWhitespace`
    implements a
    :func:`~deltas.ParagraphsSentencesAndWhitespace.segment`
    function that clusters tokens into segments of paragraph and
    sentence :class:`~deltas.segmenters.MatchableSegment` with whitespace
    :class:`~deltas.segmenters.Segment` inbetween.

:Example:
    >>> from deltas import ParagraphsSentencesAndWhitespace, text_split
    >>> from deltas.segmenters import print_tree
    >>>
    >>> a = text_split.tokenize("This comes first.  This comes second.")
    >>>
    >>> segmenter = ParagraphsSentencesAndWhitespace()
    >>> segments = segmenter.segment(a)
    >>>
    >>> print_tree(segments)
    MatchableSegment: 'This comes first.  This comes second.'
    	MatchableSegment: 'This comes first.'
    	Segment: '  '
    	MatchableSegment: 'This comes second.'
"""

from .paragraphs_sentences_and_whitespace import ParagraphsSentencesAndWhitespace
from .segmenter import Segmenter
from .segments import Segment, MatchableSegment
from .functions import print_tree
