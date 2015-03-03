import re

import yamlconf

from .token import Token


class Token(Token):
    __slots__ = ("i", "start", "end", "type")
    def __new__(cls, *args, **kwargs):
        return str.__new__(cls, args[0])

class Tokenizer:
    
    def tokenize(self, text):
        raise NotImplementedError()
    
class RegexTokenizer(Tokenizer):
    """
    Uses a lexicon of regular expressions and names to tokenize a text string.
    """
    def __init__(self, lexicon):
        self.lexicon = lexicon
        self.regex = re.compile('|'.join('(?P<{0}>{1})'.format(name, pattern)
                                         for name, pattern in lexicon))
    
    def tokenize(self, text):
        
        for i, match in enumerate(self.regex.finditer(text)):
            type = match.lastgroup
            value = match.group(0)
            
            #yield Token(value, i=i, type=type)
            #yield (value, i, type)
            token = Token(value)
            token.i = i
            token.start = i
            token.end = i+1
            token.type = type
            yield token
