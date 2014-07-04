from nose.tools import eq_
import re
from ...segmenters import ParagraphsSentencesAndWhitespace
from ..apply import apply
from ..segment_matcher import diff
from .. import util


def test_diff():
    a_tokens = [
        'This', ' ', 'is', ' ', 'some', ' ', 'text', '.',
        ' ',
        'This', ' ', 'is', ' ', 'some', ' ', 'other', ' ', 'text', '.',
        '  \n\n',
        'Starting', ' ', 'a', ' ', 'new', ' ', 'paragraph', '.',
        '  ',
        'I', ' ', 'like', ' ', 'pees', '!'
    ]
    b_tokens = [
        'This', ' ', 'is', ' ', 'some', ' ', 'text', '.',
        ' ',
        'This', ' ', 'is', ' ', 'some', ' ', 'other', ' ', 'text', '.',
        '  \n\n',
        'Starting', ' ', 'a', ' ', 'new', ' ', 'paragraph', '.',
        '  ',
        'This', ' ', 'is', ' ', 'some', ' ', 'text', '.',
        '  ',
        'I', ' ', 'like', ' ', 'pees', '!'
    ]
    segmenter = ParagraphsSentencesAndWhitespace(
        whitespace = re.compile("[\\r\\n\\t\\ ]+"),
        paragraph_split = re.compile("[\\t\\ \\r]*[\n][\\t\\ \\r]*[\n][\\t\\ \\r]*"),
        sentence_end = re.compile("[.?!]+")
    )
    ops = list(diff(a_tokens, b_tokens, segmenter))
    replay_b_tokens = list(str(t) for t in apply(ops, a_tokens))
    
    print(b_tokens)
    print(replay_b_tokens)
    eq_(b_tokens, replay_b_tokens)

def test_diff_and_replay():
    segmenter = ParagraphsSentencesAndWhitespace(
        whitespace = re.compile("[\\r\\n\\t\\ ]+"),
        paragraph_split = re.compile("[\\t\\ \\r]*[\n][\\t\\ \\r]*[\n][\\t\\ \\r]*"),
        sentence_end = re.compile("[.?!]+")
    )
    diff_func = lambda a, b:diff(a, b, segmenter=segmenter)
    return util.test_diff_and_replay(diff_func)
