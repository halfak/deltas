import re

from nose.tools import eq_

from ...tokenizers import Token, wikitext_split
from ..paragraphs_sentences_and_whitespace import \
    ParagraphsSentencesAndWhitespace
from ..segments import MatchableSegment, Segment


def test_segment():

    segmenter = ParagraphsSentencesAndWhitespace()

    text = 'This is some text.  This is some other text.\n ' + \
           'A. Peterson is a name that I made up.\n' + \
           'This is an additional sentence.\n' + \
           '\n' + \
           '== OMG HEADER ==\n' + \
           'This is a new paragraph! Isn\'t this fun?'

    tokens = wikitext_split.tokenize(text)
    segments = list(segmenter.segment(tokens))
    print([str(s) for s in segments[0]])

    eq_(len(segments), 3)  # 2 paragraphs + 1 whitespace

    eq_(len(segments[0]), 8)  # 4 sentences + 4 whitespace

    eq_(type(segments[1]), Segment)
    eq_(type(segments[2]), MatchableSegment)
    eq_(type(segments[2][2]), MatchableSegment)

    eq_(''.join(str(s) for s in segments), text)
