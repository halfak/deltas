"""
Tokenizers are used to split text content into a sequence of tokens.  Extend
:class:`~deltas.tokenizers.Tokenizer` to implement a custom tokenizer.

:class:`~deltas.tokenizers.TextSplit`
    implements a :func:`~deltas.tokenizers.TextSplit.tokenize` function that
    splits text into words, punctuation, symbols and whitespace.
    

"""
from .tokenizer import Tokenizer
from .text_split import TextSplit
from .wikitext_split import WikitextSplit
