Deltas
======

An open licensed (MIT) library for performing generating deltas (A.K.A sequences
of operations) representing the difference between two sequences of comparable
tokens.

* **Installation:** ``pip install deltas``
* **Repo**: http://github.com/halfak/Deltas
* **Documentation**: http://pythonhosted.org/deltas
* Note this library requires Python 3.3 or newer

This library is intended to be used to make experimental difference detection
strategies more easily available.  There are currently two strategies available:

``deltas.sequence_matcher.diff(a, b)``:
    A shameless wrapper around `difflib.SequenceMatcher` to get it to work
    within the structure of *deltas*.
``deltas.segment_matcher.diff(a, b, segmenter=None)``:
    A generalized difference detector that is designed to detect block moves
    and copies based on the use of a ``Segmenter``.

:Example:
    >>> from deltas import segment_matcher, text_split
    >>>
    >>> a = text_split.tokenize("This is some text.  This is some other text.")
    >>> b = text_split.tokenize("This is some other text.  This is some text.")
    >>> operations = segment_matcher.diff(a, b)
    >>>
    >>> for op in operations:
    ...     print(op.name, repr(''.join(a[op.a1:op.a2])),
    ...           repr(''.join(b[op.b1:op.b2])))
    ...
    equal 'This is some other text.' 'This is some other text.'
    insert ' ' '  '
    equal 'This is some text.' 'This is some text.'
    delete '  ' ''


Tokenization
============

By default Deltas performs tokenization by regexp text splitting. 
We included CJK tokenization functionality. If text consists of at least 1/4
Japanse or Korean symbols it is Tokenized by language specific Tokenizer.
Else, Chinese Tokenizer is used.

Chinese Tokenizer - Jieba
Japanese Tokenizer - Sudachi
Korean Tokenizer - KoNLPy(Okt)

:CJK Tokenization example:
import mwapi
import deltas
import deltas.tokenizers

session = mwapi.Session("https://zh.wikipedia.org")
doc = session.get(action="query", prop="revisions",
                  titles="中国", rvprop="content", rvslots="main",
                  formatversion=2)
text = doc['query']['pages'][0]['revisions'][0]['slots']['main']['content']

tokenized_text = deltas.tokenizers.wikitext_split.tokenize(text)
tokenized_text_cjk = deltas.tokenizers.wikitext_split_w_cjk.tokenize(text)

FOR IMPROVED JAPANESE TOKENIZER ACCURACY INSTALL FULL DICTIONARY
================================================================

```
pip install sudachidict_full
# and link sudachi to dict
sudachipy link -t full
```