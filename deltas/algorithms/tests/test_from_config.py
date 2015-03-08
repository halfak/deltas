from nose.tools import eq_

from ...tokenizers import wikitext_split
from ..engine import Engine


def test_from_config():
    doc = {
        'engines': {
            'segment_matcher':{
                'class': "deltas.algorithms.SegmentMatcher",
                'segmenter': "western_psw",
                'tokenizer': "wikitext_split"
            }
        },
        'segmenters': {
            'western_psw': {
                'class': "deltas.segmenters.ParagraphsSentencesAndWhitespace"
            }
        },
        'tokenizers': {
            'wikitext_split': {
                'module': "deltas.tokenizers.wikitext_split"
            }
        }
    }

    segment_matcher = Engine.from_config(doc, "segment_matcher")
    text_operations = list(segment_matcher.process(["Foo bar.", "Foo burp."]))
    eq_(len(text_operations), 2)
    
    ops, a, b = text_operations[1]
    eq_(len(list(ops)), 4)
