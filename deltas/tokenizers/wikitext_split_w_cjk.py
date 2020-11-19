
from .tokenizer import TokenizerPipeline
from .tokenizer import CJKProcessor
from .wikitext_split import wikitext_split
from . import lexicon_chars

CJK_LEXICON = {
    'cjk': r'['+lexicon_chars.cjk+r']',
    'japanese': r'['+lexicon_chars.jap_char+r']',
    'korean': r'['+lexicon_chars.kor_char+r']',
}

wikitext_split_w_cjk = TokenizerPipeline(wikitext_split,
                                         CJKProcessor(CJK_LEXICON))
