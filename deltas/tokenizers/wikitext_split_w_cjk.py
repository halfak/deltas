from .tokenizer import TokenizerPipeline
from .tokenizer import CJKProcessor
from .tokenizer import RegexTokenizer
from . import lexicon

wikitext_split_w_cjk = TokenizerPipeline(RegexTokenizer(lexicon.WIKITEXT_SPLIT_LEXICON),
                                         CJKProcessor(lexicon.CJK_LEXICON))
