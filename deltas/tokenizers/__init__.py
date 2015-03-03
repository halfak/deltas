"""
Tokenizers are used to split text content into a sequence of tokens.  Extend
:class:`~deltas.tokenizers.Tokenizer` to implement a custom tokenizer.

:class:`~deltas.tokenizers.text_split`
    implements a :func:`~deltas.tokenizers.text_split.tokenize` function that
    splits text into words, punctuation, symbols and whitespace.


"""
from .tokenizer import Tokenizer
from .token import Token
from .text_split import text_split
from .wikitext_split import wikitext_split
