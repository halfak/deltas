Deltas
======

An open licensed (MIT) library for performing generating deltas (A.K.A sequences
 of operations) representing the difference between two sequences of comparable
tokens.

* **Installation:** **TODO**
* **Repo**: `http://github.com/halfak/Deltas`_

This library is intended to be used to make experimental difference detection
strategies more easily available.  There are currently two strategies available:

``deltas.sequence_matcher.diff(a, b)``:
    A shameless wrapper around `difflib.SequenceMatcher` to get it to work
    within the structure of *deltas*.
``deltas.sequence_matcher.diff(a, b, segmenter=None)``:
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
    
