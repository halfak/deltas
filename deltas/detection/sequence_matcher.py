"""
Match sequences (longest common substring)
------------------------------------------

Performs a simple *longest-common-substring* diff.  This module implements a
simple wrapper around :class:`difflib.SequenceMatcher`.

:Example:
    >>> from deltas import sequence_matcher, apply
    >>>
    >>> a_tokens = ["This", " ", "comes", " ", "first", ".",
    ...             " ",
    ...             "This", " ", "comes", " ", "second", "."]
    >>>
    >>> b_tokens = ["This", " ", "comes", " ", "second", ".",
    ...             " ",
    ...             "This", " ", "comes", " ", "first", "."]
    >>>
    >>> operations = sequence_matcher.diff(a_tokens, b_tokens)
    >>>
    >>> for operation in operations:
    ...     print(operation)
    ...
    Insert(name='insert', a1=0, a2=0, b1=0, b2=7)
    Equal(name='equal', a1=0, a2=6, b1=7, b2=13)
    Delete(name='delete', a1=6, a2=13, b1=13, b2=13)
"""

from difflib import SequenceMatcher as SM

from ..operations import Insert, Equal, Delete

def parse_replace(a1, a2, b1, b2):
    yield Delete(a1, a2, b1, b2)
    yield Insert(a1, a2, b1, b2)

def parse_insert(a1, a2, b1, b2):
    yield Insert(a1, a2, b1, b2)

def parse_delete(a1, a2, b1, b2):
    yield Delete(a1, a2, b1, b2)

def parse_equal(a1, a2, b1, b2):
    yield Equal(a1, a2, b1, b2)

OP_PARSERS = {
    "replace": parse_replace,
    "insert": parse_insert,
    "delete": parse_delete,
    "equal": parse_equal
}

def parse_opcodes(opcodes):
    
    for opcode in opcodes:
        op, a_start, a_end, b_start, b_end = opcode
        
        parse = OP_PARSERS[op]
        for operation in parse(a_start, a_end, b_start, b_end):
            yield operation
    

def diff(a, b):
    """
    Performs a longest common substring diff.
    
    :Parameters:
        a : sequence of `comparable`
            Initial sequence
        b : sequence of `comparable`
            Changed sequence
    
    :Returns:
        An `iterable` of operations.
    """
    opcodes = SM(None, a, b).get_opcodes()
    return parse_opcodes(opcodes)
