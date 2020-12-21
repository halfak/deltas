"""
Tokenizers are used to split text content into a sequence of tokens.  Extend
:class:`~deltas.Tokenizer` to implement a custom tokenizer.  See
also :class:`~deltas.RegexTokenizer` for producing a tokenizer
based on a lexicon.

**deltas.text_split**
    a :class:`~deltas.RegexTokenizer` that splits text into words,
    punctuation, symbols and whitespace.

**deltas.wikitext_split**
    a :class:`~deltas.RegexTokenizer` that splits text into words,
    punctuation, symbols and whitespace as well as wikitext markup elements
    (e.g. ('dcurly_open', "{{") and ('bold', "'''"))

**deltas.wikitext_spli_w_cjk**
    a :class:`~deltas.TokenizerPipeline` that splits text into words,
    punctuation, symbols and whitespace as well as wikitext markup elements
    (e.g. ('dcurly_open', "{{") and ('bold', "'''")) and performs additional
    tokenization of 'cjk_word' tokens
"""
from .tokenizer import Tokenizer, RegexTokenizer, CJKProcessor, TokenizerPipeline # noqa
from .token import Token
from .text_split import text_split
from .wikitext_split import wikitext_split
from .wikitext_split_w_cjk import wikitext_split_w_cjk
from .cjk_tokenization import lng_decision, CJK_tokenization


__all__ = [Tokenizer, RegexTokenizer, CJKProcessor, TokenizerPipeline, Token, text_split, wikitext_split, wikitext_split_w_cjk, lng_decision, CJK_tokenization] # noqa
