import re
import yamlconf
from .token import Token
from . import cjk_tokenization


class Tokenizer:
    """
    Constructs a tokenizaton strategy.
    """
    def tokenize(self, text, token_class=Token):
        """
        Tokenizes a text.
        """
        raise NotImplementedError()

    @classmethod
    def from_config(cls, config, name, section_key="tokenizers"):
        section = config[section_key][name]
        if 'module' in section:
            return yamlconf.import_module(section['module'])
        else:
            Tokenizer = yamlconf.import_module(section['class'])
            return Tokenizer.from_config(config, name, section_key)


class RegexTokenizer(Tokenizer):
    """
    Uses a lexicon of regular expressions and names to tokenize a text string.
    """
    def __init__(self, lexicon):
        self.lexicon = lexicon
        self.regex = re.compile('|'.join('(?P<{0}>{1})'.format(name, pattern)
                                         for name, pattern in lexicon))

    def tokenize(self, text, token_class=None):
        return [t for t in self._tokenize(text, token_class=token_class)]

    def _tokenize(self, text, token_class=None):
        """
        Tokenizes a text

        :Returns:
            A `list` of tokens
        """
        token_class = token_class or Token
        tokens = {}

        for i, match in enumerate(self.regex.finditer(text)):
            value = match.group(0)

            try:
                token = tokens[value]
            except KeyError:
                type = match.lastgroup
                token = token_class(value, type=type)
                tokens[value] = token

            yield token


class TokenizerPipeline(Tokenizer):
    def __init__(self, tokenizer, *token_processors):
        self.tokenizer = tokenizer  # start of the pipeline
        self.token_processors = token_processors

    def tokenize(self, text):
        tokens = self.tokenizer.tokenize(text)
        for token_processor in self.token_processors:
            tokens = token_processor.process(tokens)
        return tokens


class TokenProcessor:
    def process(self, tokenized_text):
        raise NotImplementedError()


class CJKProcessor(TokenProcessor):
    """
    Uses a cjk_lexicon to decide which tokenizer should be used
    (Chinese, Japanese or Korean).
    """
    def __init__(self, cjk_lexicon, lng_frac_par=0.25):
        self.cjk_lexicon = cjk_lexicon
        self.lng_frac_par = lng_frac_par

    def process(self, tokenized_text, token_class=None):
        token_class = token_class or Token
        language = self._lng_decision(tokenized_text)
        processed_tokens = self._cjk_processing(tokenized_text,
                                                language=language,
                                                token_class=token_class)
        return processed_tokens

    def _lng_decision(self, tokenized_text):
        text = "".join([tok[:]
                        for tok in tokenized_text
                        if tok.type == 'cjk_word'])
        language = cjk_tokenization.lng_decision(text, self.cjk_lexicon,
                                                 self.lng_frac_par)
        return language

    def _cjk_processing(self, tokenized_text, language, token_class=None):
        token_class = token_class or Token
        cjk_word_indices = list(filter(
                                lambda x:
                                tokenized_text[x].type == 'cjk_word',
                                range(len(tokenized_text))))

        # go from the last to first,
        # "unpack" CJK "words" and assign "cjk_word" to them
        for i in cjk_word_indices[::-1]:
            proc_cjk_token = cjk_tokenization.CJK_tokenization(
                                           tokenized_text[i], language)
            tokenized_text[i:i+1] = [token_class(word, type="cjk_word")
                                     for word in proc_cjk_token]

        return tokenized_text
