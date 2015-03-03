"""
Provides a segmenter for splitting text tokens into
:class:`~deltas.segmenters.paragraphs_sentences_and_whitespace.Paragraph`,
:class:`~deltas.segmenters.paragraphs_sentences_and_whitespace.Sentence`, and
:class:`~deltas.segmenters.paragraphs_sentences_and_whitespace.Whitespace`.


.. autoclass:: deltas.segmenters.ParagraphsSentencesAndWhitespace
    :members:
.. autoclass:: deltas.segmenters.paragraphs_sentences_and_whitespace.Paragraph
.. autoclass:: deltas.segmenters.paragraphs_sentences_and_whitespace.Sentence
.. autoclass:: deltas.segmenters.paragraphs_sentences_and_whitespace.Whitespace
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
    def __init__(self, *, whitespace=None,
                          paragraph_end=None,
                          sentence_end=None,
                          min_sentence=None):
        
        self.whitespace = set(whitespace or WHITESPACE)
        self.paragraph_end = set(paragraph_end or PARAGRAPH_END)
        self.sentence_end = set(sentence_end or SENTENCE_END)
        self.min_sentence = int(min_sentence or MIN_SENTENCE)
    
    def segment(self, tokens):
        
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
    
    '''
    def segment(self, tokens):
        """
        Clusters a sequence of tokens into a list of segments.
        
        :Parameters:
            tokens : `iterable` of `str`
                A series of tokens to segment.
        
        :Returns:
            A `list` of :class:`Segment`
        """
        look_ahead = LookAhead(tokens)

        while look_ahead.peek(None) is not None:
            if look_ahead.peek().type in self.whitespace:
                segment = self._read_whitespace(look_ahead)
            else:
                segment = self._read_paragraph(look_ahead)
                
            yield segment
    '''
    
    def _read_whitespace(self, look_ahead):
        
        whitespace = Segment([next(look_ahead)])
        
        while look_ahead.peek(None) is not None and \
              look_ahead.peek().type in self.whitespace:
            whitespace.append(next(look_ahead))
            
        
        return whitespace
    
    def _read_sentence(self, look_ahead):
        
        sentence = MatchableSegment([next(look_ahead)])
        
        while look_ahead.peek(None) is not None and \
              look_ahead.peek() not in self.paragraph_end:
            
            sentence_bit = next(look_ahead)
            sentence.append(sentence_bit)
            
            if sentence_bit.type in self.sentence_end:
                non_whitespace = sum(s.type not in self.whitespace for s in sentence)
                if non_whitespace >= self.min_sentence:
                    break
            
        return sentence
    
    def _read_paragraph(self, look_ahead):
        
        paragraph = MatchableSegment()
        
        while look_ahead.peek(None) is not None and \
              look_ahead.peek().type not in self.paragraph_end:
            
            if look_ahead.peek().type in self.whitespace:
                segment = self._read_whitespace(look_ahead)
            else:
                segment = self._read_sentence(look_ahead)
                
            paragraph.append(segment)
        
        return paragraph
    
    @classmethod
    def from_config(cls, doc, name):
        subsection = doc['segmenters'][name]
        return cls(
            whitespace=subsection.get('whitespace'),
            paragraph_end=subsection.get('paragraph_end'),
            sentence_end=subsection.get('sentence_end'),
            min_sentence=subsection.get('min_sentence')
        )
