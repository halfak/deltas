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
