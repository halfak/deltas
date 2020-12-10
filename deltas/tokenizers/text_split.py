from .tokenizer import RegexTokenizer
from . import lexicon

text_split = RegexTokenizer(lexicon.TEXT_SPLIT_LEXICON)
