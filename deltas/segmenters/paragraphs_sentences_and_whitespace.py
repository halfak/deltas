"""
Provides a segmenter for splitting text tokens into whitespace
:class:`~deltas.segmenters.Segment` and paragraphs
:class:`~deltas.segmenters.MatchableSegment` which contain sentence
:class:`~deltas.segmenters.MatchableSegment` and whitespace
:class:`~deltas.segmenters.Segment`.

.. autoclass:: deltas.segmenters.ParagraphsSentencesAndWhitespace
    :members:
"""
import re

from more_itertools import peekable

from ..util import LookAhead
from .segmenter import Segmenter
from .segments import MatchableSegment, Segment

WHITESPACE = set(["whitespace", "break"])
PARAGRAPH_END = set(["break"])
SENTENCE_END = set(["period", "epoint", "qmark"])
MIN_SENTENCE = 5

class ParagraphsSentencesAndWhitespace(Segmenter):
    """
    Constructs a paragraphs, sentences and whitespace segmenter.  This segmenter
    is intended to be used in western languages where sentences and paragraphs
    are meaningful segments of text content.
    
    :Parameters:
        whitespace : `set`(`str`)
            A set of token types that represent whitespace.
        paragraph_end : `set`(`str`)
            A set of token types that represent the end of a pragraph.
        sentence_end : `set`(`str`)
            A set of tokens types that represent the end of a sentence.
        min_sentence : int
            The minimum non-whitespace tokens that a sentence must contain
            before a sentence_end will be entertained.
    """
    def __init__(self, *, whitespace=None,
                          paragraph_end=None,
                          sentence_end=None,
                          min_sentence=None):
        
        self.whitespace = set(whitespace or WHITESPACE)
        self.paragraph_end = set(paragraph_end or PARAGRAPH_END)
        self.sentence_end = set(sentence_end or SENTENCE_END)
        self.min_sentence = int(min_sentence or MIN_SENTENCE)
    
    def segment(self, tokens):
        """
        Segments a sequence of tokens into a sequence of segments.
        
        :Parameters:
            tokens : `list`(`deltas.tokenizers.Token`)
        """
        look_ahead = LookAhead(tokens)

        segments = []

        while not look_ahead.empty():
            
            if look_ahead.peek().type not in self.whitespace: # Paragraph!
                paragraph = MatchableSegment()
                
                while not look_ahead.empty() and \
                      look_ahead.peek().type not in self.paragraph_end:

                    if look_ahead.peek().type not in self.whitespace: #Sentence!
                        sentence = MatchableSegment([next(look_ahead)])
                        
                        while not look_ahead.empty() and \
                              look_ahead.peek().type not in self.paragraph_end:
                            
                            sentence.append(next(look_ahead))
                            
                            if sentence[-1].type in self.sentence_end:
                                non_whitespace = sum(s.type not in self.whitespace for s in sentence)
                                if non_whitespace >= self.min_sentence:
                                    break
                            
                        
                        paragraph.append(sentence)
                        
                    else:
                        whitespace = Segment([next(look_ahead)])
                        paragraph.append(whitespace)
                
                segments.append(paragraph)
            else:
                whitespace = Segment([next(look_ahead)])
                segments.append(whitespace)
            
        
        return segments
    
    @classmethod
    def from_config(cls, doc, name):
        subsection = doc['segmenters'][name]
        return cls(
            whitespace=subsection.get('whitespace'),
            paragraph_end=subsection.get('paragraph_end'),
            sentence_end=subsection.get('sentence_end'),
            min_sentence=subsection.get('min_sentence')
        )
