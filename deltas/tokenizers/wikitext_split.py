from .tokenizer import RegexTokenizer
from . import lexicon

wikitext_split = RegexTokenizer(lexicon.WIKITEXT_SPLIT_LEXICON)
