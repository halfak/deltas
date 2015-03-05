import re
from collections import namedtuple

import yamlconf

from .token import Token


class Tokenizer:
    """
    Constructs a tokenizaton strategy.
    """
    def tokenize(self, text):
        """
        Tokenizes a text.
        """
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
        return [t for t in self._tokenize(text)]
    
    def _tokenize(self, text):
        """
        Tokenizes a text
        
        :Returns:
            A `list` of tokens
        """
        for i, match in enumerate(self.regex.finditer(text)):
            type = match.lastgroup
            value = match.group(0)
            
            yield Token(value, i, type)
