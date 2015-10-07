Deltas -- Experimental Difference Algorithms
============================================
This library provides utilities for generating deltas (A.K.A sequences of operations) representing the difference between two sequences of comparable  tokens.  This library is intended to be used to make experimental difference detection strategies more easily available.

* **Installation:** ``pip install deltas``
* **Documentation:** https://pythonhosted.org/deltas
* **Repository:** http://github.com/halfak/deltas
* **License:** MIT

Contents
--------
.. toctree::
    :maxdepth: 1

    algorithms
    operations
    tokenizers
    segmenters
    apply

Example
-------
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

Author
======
* Aaron Halfaker -- https://github.com/halfak

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
