FOLLOW THESE INSTRUCTIONS BEFORE USING CJK TOKENIZATION
=======================================================
* **CHINESE**
* install pkuseg
```
pip install pkuseg
```
* **JAPANESE**
* install mecab 
```
wget -O mecab-0.996.tar.gz "https://drive.google.com/uc?export=download&id=0B4y35FiV1wh7cENtOXlicTFaRUE"
tar zxvf mecab-0.996.tar.gz
cd mecab-0.996 && ./configure && make && make check
sudo make install
```
* install mecab ipadic dictionary
```
wget -O mecab-ipadic-2.7.0-20070801.tar.gz "https://drive.google.com/uc?export=download&id=0B4y35FiV1wh7MWVlSDBCSXZMTXM"
tar zxvf mecab-ipadic-2.7.0-20070801.tar.gz
cd mecab-ipadic-2.7.0-20070801 &&./configure --with-charset=utf8 && make && make check
sudo make install
```
* **KOREAN**
* install konlpy
```
pip install konlpy
```
* install Mecab-ko dictionary
```
wget https://bitbucket.org/eunjeon/mecab-ko-dic/downloads/mecab-ko-dic-1.6.1-20140814.tar.gz
tar zxfv mecab-ko-dic-1.6.1-20140814.tar.gz
cd mecab-ko-dic-1.6.1-20140814
./configure
sudo ldconfig
make
sudo sh -c 'echo "dicdir=/usr/local/lib/mecab/dic/mecab-ko-dic" > /usr/local/etc/mecabrc'
sudo make install
```

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
