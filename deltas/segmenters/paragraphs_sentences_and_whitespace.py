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
from .segmenter import Segmenter
from .segments import Token, MatchableSegmentNodeCollection, \
                      MatchableTokenSequence, TokenSequence
from ..util import LookAhead

WHITESPACE_RE = re.compile("[\\r\\n\\t\\ ]+")
PARAGRAPH_SPLIT_RE = re.compile("[\\t\\ \\r]*[\n][\\t\\ \\r]*[\n][\\t\\ \\r]*")
SENTENCE_END_RE = re.compile("[.?!]+")
MIN_SENTENCE_RE = 5

class Paragraph(MatchableSegmentNodeCollection):
    """
    A paragraph (matchable)
    """
    pass
class Sentence(MatchableTokenSequence):
    """
    A sentence (matchable)
    """
    pass
class Whitespace(TokenSequence):
    """
    Some whitespace (unmatchable)
    """
    pass

class ParagraphsSentencesAndWhitespace(Segmenter):
    """
    Constructs a segmenter that clusters text into :class:`Paragraph`,
    :class:`Sentence` and :class:`Whitespace` segments.  Paragraphs and
    sentences are matchable, while whitespace is not matchable.
    
    :Parameters:
        whitespace : :class:`SRE_Pattern`
            A regular expression pattern that matches whitespace tokens.
        paragraph_split : :class:`SRE_Pattern`
            A regular expression pattern that matches paragraph delimiting
            tokens.
        sentence_end : :class:`SRE_Pattern`
            A regular expression pattern that matches the end of paragraphs
        min_sentence : int
            The minimum sentence length before accepting a sentence_end token.
    """
    def __init__(self, *, whitespace=WHITESPACE_RE,
                          paragraph_split=PARAGRAPH_SPLIT_RE,
                          sentence_end=SENTENCE_END_RE,
                          min_sentence=MIN_SENTENCE_RE):
        
        
        if not hasattr(whitespace, "match"):
            raise TypeError("whitespace is the wrong type." + \
                            "Expected {0}, ".format(type(re.compile(" "))) + \
                            "got {0}".format(type(whitespace)))
        self.whitespace = whitespace
        
        if not hasattr(paragraph_split, "match"):
            raise TypeError("paragraph_split is the wrong type." + \
                            "Expected {0}, ".format(type(re.compile(" "))) + \
                            "got {0}".format(type(paragraph_split)))
        self.paragraph_split = paragraph_split
                
        
        if not hasattr(sentence_end, "match"):
            raise TypeError("sentence_end is the wrong type." + \
                            "Expected {0}, ".format(type(re.compile(" "))) + \
                            "got {0}".format(type(sentence_end)))
        self.sentence_end = sentence_end
        
        self.min_sentence = int(min_sentence)
    
    def segment(self, tokens):
        """
        Clusters a sequence of tokens into a list of segments.
        
        :Parameters:
            tokens : `iterable` of `str`
                A series of tokens to segment.
        
        :Returns:
            A `list` of :class:`Segment`
        """
        self.look_ahead = LookAhead(tokens)

        segments = []

        while not self.look_ahead.empty():
            if self.whitespace.match(self.look_ahead.peek()):
                segment = self._read_whitespace(self.look_ahead)
            else:
                segment = self._read_paragraph(self.look_ahead)
                
            segments.append(segment)

        return segments
    
    def _read_whitespace(self, look_ahead):
        #print("Reading whitespace.")
        
        whitespace_tokens = []
        
        while not look_ahead.empty() and \
              self.whitespace.match(self.look_ahead.peek()):
            whitespace_tokens.append(Token(look_ahead.i, look_ahead.pop()))
            
        
        return Whitespace(whitespace_tokens)
    
    def _read_sentence(self, look_ahead):
        #print("Reading sentence.")
        
        sentence_tokens = []
        
        while not look_ahead.empty() and \
              not self.paragraph_split.match(look_ahead.peek()):
            
            i, sentence_bit = look_ahead.i, look_ahead.pop()
            sentence_tokens.append(Token(i, sentence_bit))
            
            if self.sentence_end.match(sentence_bit) and \
               len(sentence_tokens) >= self.min_sentence:
                break
            
        return Sentence(sentence_tokens)
    
    def _read_paragraph(self, look_ahead):
        #print("Reading paragraph.")
        
        segments = []
        
        while not look_ahead.empty() and \
              not self.paragraph_split.match(look_ahead.peek()):
            
            if self.whitespace.match(look_ahead.peek()):
                segment = self._read_whitespace(look_ahead)
            else:
                segment = self._read_sentence(look_ahead)
                
            segments.append(segment)
        
        return Paragraph(segments)
    
