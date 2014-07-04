from nose.tools import eq_

import re
from ..segments import Token
from ..paragraphs_sentences_and_whitespace import Paragraph, Sentence, \
                                                  Whitespace, \
                                                  ParagraphsSentencesAndWhitespace

def test_segment():
    
    tokens = [
        'This', ' ', 'is', ' ', 'some', ' ', 'text', '.', ' ',
        'This', ' ', 'is', ' ', 'some', ' ', 'other', ' ', 'text', '.', '  ',
        'A', '.', ' ', 'J', '.', ' ', 'Peterson', ' ', 'is', ' ', 'a', ' ', 'name', ' ', 'that', ' ', 'I', ' ', 'made', ' ', 'up', '.', '\n',
        'This', ' ', 'is', ' ', 'an', ' ', 'additional', ' ', 'sentence', '.', '\n\n',
        
        'This', ' ', 'is', ' ', 'a', ' ', 'new', ' ', 'paragraph', '!', '  ',
        'Isn', "'", 't', ' ', 'this', ' ', 'fun', '?'
    ]
    expected = [
        Paragraph(
            [
                Sentence(Token(i, c) for i, c in zip(range(0, 8), tokens[0:8])),
                Whitespace(Token(i, c) for i, c in zip(range(8, 9), tokens[8:9])),
                Sentence(Token(i, c) for i, c in zip(range(9, 19), tokens[9:19])),
                Whitespace(Token(i, c) for i, c in zip(range(19, 20), tokens[19:20])),
                Sentence(Token(i, c) for i, c in zip(range(20, 42), tokens[20:42])),
                Whitespace(Token(i, c) for i, c in zip(range(42, 43), tokens[42:43])),
                Sentence(Token(i, c) for i, c in zip(range(43, 53), tokens[43:53]))
            ]
        ),
        Whitespace(Token(i, c) for i, c in zip(range(53, 54), tokens[53:54])),
        Paragraph(
            [
                Sentence(Token(i, c) for i, c in zip(range(54, 64), tokens[54:64])),
                Whitespace(Token(i, c) for i, c in zip(range(64, 65), tokens[64:65])),
                Sentence(Token(i, c) for i, c in zip(range(65, 73), tokens[65:73]))
            ]
        )
    ]
    
    segmenter = ParagraphsSentencesAndWhitespace(
        whitespace = re.compile("[\\r\\n\\t\\ ]+"),
        paragraph_split = re.compile("[\\t\\ \\r]*[\n][\\t\\ \\r]*[\n][\\t\\ \\r]*"),
        sentence_end = re.compile("[.?!]+")
    )
    segments = segmenter.segment(tokens)
    
    print(segments);print(expected)
    eq_(segments, expected)

def test_equality():
    eq_(Sentence([Token(0, "zero"), Token(1, "one")]),
        Sentence([Token(10, "zero"), Token(11, "one")]))
    eq_(Paragraph([
            Sentence([Token(0, "zero"), Token(1, "one")]),
            Sentence([Token(2, "two"), Token(3, "three")])
        ]),
        Paragraph([
            Sentence([Token(10, "zero"), Token(11, "one")]),
            Sentence([Token(12, "two"), Token(13, "three")])
        ]),
    )
