.. Deltas documentation master file, created by
   sphinx-quickstart on Fri Jul  4 14:02:59 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Deltas -- Experimental Difference Algorithms
============================================
**Deltas** is an open licensed (MIT) library for performing generating deltas
(A.K.A sequences of operations) representing the difference between two
sequences of comparable  tokens.

* **Installation:** ``pip install deltas``
* **Repository:** `http://github.com/halfak/Deltas <http://github.com/halfak/Deltas>`_

This library is intended to be used to make experimental difference detection
strategies more easily available.  There are currently two strategies available:

:class:`~deltas.detection.sequence_matcher`:
    A shameless wrapper around `difflib.SequenceMatcher` to get it to work
    within the structure of *deltas*.
:class:`~deltas.detection.segment_matcher`:
    A generalized difference detector that is designed to detect block moves
    and copies based on the use of a ``Segmenter``.
    

:Example:
    >>> from deltas import segment_matcher, apply
    >>>
    >>> a_tokens = ["This", " ", "comes", " ", "first", ".",
    ...             " ",
    ...             "This", " ", "comes", " ", "second", "."]
    >>>
    >>> b_tokens = ["This", " ", "comes", " ", "second", ".",
    ...             " ",
    ...             "This", " ", "comes", " ", "first", "."]
    >>>
    >>> operations = segment_matcher.diff(a_tokens, b_tokens)
    >>>
    >>> for operation in operations:
    ...     print(operation)
    ...
    Equal(name='equal', a1=7, a2=13, b1=0, b2=6)
    Insert(name='insert', a1=6, a2=7, b1=6, b2=7)
    Equal(name='equal', a1=0, a2=6, b1=7, b2=13)
    Delete(name='delete', a1=6, a2=7, b1=13, b2=13)

Detect differences
------------------
.. automodule:: deltas.detection

Operations
----------
.. automodule:: deltas.operations

Tokenizers
----------
.. automodule:: deltas.tokenizers

Segmenters
----------
.. automodule:: deltas.segmenters


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
