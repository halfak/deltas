from nose.tools import eq_

from ..tokenizer import Tokenizer


def test_from_config():
    doc = {
        'tokenizers': {
            'text_split': {
                'class': 'deltas.tokenizers.TextSplit'
            }
        }
    }
    
    text_split = Tokenizer.from_config(doc, "text_split")
    
    eq_(list(text_split.tokenize("Foo bar")), ["Foo", " ", "bar"])
