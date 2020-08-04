
from .tokenizer import TokenizerPipeline
from .tokenizer import CJKProcessor
from .wikitext_split import wikitext_split
from .lexikon_chars import *

CJK_LEXICON = {
    'cjk': r'['+cjk+r']',
    'japanese': r'['+jap_char+r']',
    'korean': r'['+kor_char+r']',
}

wikitext_split_w_cjk = TokenizerPipeline(wikitext_split, CJKProcessor(CJK_LEXICON)) # noqa
