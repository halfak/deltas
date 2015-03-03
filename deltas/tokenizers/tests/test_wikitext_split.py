from nose.tools import eq_

from ..wikitext_split import wikitext_split


def test_wikitext_split():
    
    
    input = "As a sentence, this includes punctuation. \n" + \
            "\n" + \
            "==Header!==" + \
            "And then we have another sentence here!"
    
    expected = ['As', ' ', 'a', ' ', 'sentence', ',', ' ', 'this', ' ',
                'includes', ' ', 'punctuation', '.', ' \n\n',
                '==', 'Header', '!', '==', 'And', ' ',
                'then', ' ', 'we', ' ', 'have', ' ', 'another', ' ', 'sentence',
                ' ', 'here', '!']
    
    tokens = list(wikitext_split.tokenize(input))
    
    eq_(tokens, expected)
