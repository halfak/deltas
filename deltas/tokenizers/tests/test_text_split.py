from nose.tools import eq_

from ..text_split import TextSplit

def test_simple_text_split():
    
    tokenizer = TextSplit()
    
    
    input = "As a sentence, this includes punctuation. \n" + \
            "\n" + \
            "And then we have another sentence here!"
    
    expected = ['As', ' ', 'a', ' ', 'sentence', ',', ' ', 'this', ' ',
                'includes', ' ', 'punctuation', '.', ' \n\n', 'And', ' ',
                'then', ' ', 'we', ' ', 'have', ' ', 'another', ' ', 'sentence',
                ' ', 'here', '!']
    
    tokens = tokenizer.tokenize(input)
    
    eq_(tokens, expected)
    
