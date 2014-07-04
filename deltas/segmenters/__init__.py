"""
Text segmentation is the process of dividing written text into meaningful units,
such as words, sentences, or topics.  This module provides a collection of
:class:`~deltas.segmenters.Segmenter` that can be used to produce hierarchical
clusters of tokens that can be understood by
:class:`~deltas.detection.segment_matcher`.

:class:`~deltas.segmenters.ParagraphsSentencesAndWhitespace`
    implements a
    :func:`~deltas.segmenters.ParagraphsSentencesAndWhitespace.segment`
    function that clusters tokens into
    :class:`~deltas.segmenters.paragraphs_sentences_and_whitespace.Paragraph`,
    :class:`~deltas.segmenters.paragraphs_sentences_and_whitespace.Sentence`, and
    :class:`~deltas.segmenters.paragraphs_sentences_and_whitespace.Whitespace`
    segments

"""

from .paragraphs_sentences_and_whitespace import ParagraphsSentencesAndWhitespace
from .segmenter import Segmenter
from .segments import IndexedSegment, MatchableSegment, Token, SegmentNode, \
                      MatchableSegmentNode, TokenSequence, \
                      MatchableTokenSequence, SegmentNodeCollection, \
                      MatchableSegmentNodeCollection
