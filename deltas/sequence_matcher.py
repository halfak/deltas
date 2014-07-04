"""
A simple wrapper around :class:`difflib.SequenceMatcher` that confirms to the
:func:`diff` API.

:Example:
	>>> from diffengine.difference import sequence_matcher
	>>>
	>>> revisions = [
	...     ['This', ' ', 'is', ' ', 'some', ' ', 'content', '.',    ' ', 'This', ' ', 'is',   ' ', 'going',   ' ', 'away', '.'],
	...     ['This', ' ', 'is', ' ', 'some', ' ', 'content', '.',    ' ', 'This', ' ', 'is',   ' ', 'new',     '.'],
	...     ['This', ' ', 'is', ' ', 'new ', '.', ' ',       'This', ' ', 'is',   ' ', 'some', ' ', 'content', '.']
	... ]
	>>> list(sequence_matcher.diff("", revisions[1]))
	[Insert(start=0, end=15)]
	>>> list(sequence_matcher.diff(revisions[1], revisions[2]))
	[Insert(start=0, end=7), Persist(start=0, end=8), Remove(start=8, end=15)]
"""

from difflib import SequenceMatcher as SM

from ..types import Insert, Persist, Remove

def parse_replace(a, b, a1, a2, b1, b2):
	yield Remove(a1, a2, a[a1:a2])
	yield Insert(b1, b2, b[b1:b2])

def parse_insert(a, b, a1, a2, b1, b2):
	yield Insert(b1, b2, b[b1:b2])

def parse_delete(a, b, a1, a2, b1, b2):
	yield Remove(a1, a2, a[a1:a2])

def parse_equal(a, b, a1, a2, b1, b2):
	assert a2 - a1 == b2 - b1
	yield Persist(a1, a2)

OP_PARSERS = {
	"replace": parse_replace,
	"insert": parse_insert,
	"delete": parse_delete,
	"equal": parse_equal
}

def parse_opcodes(opcodes, a, b):
	
	for opcode in opcodes:
		op, a_start, a_end, b_start, b_end = opcode
		
		parse = OP_PARSERS[op]
		for operation in parse(a, b, a_start, a_end, b_start, b_end):
			yield operation
	

def diff(a, b):
	opcodes = SM(None, a, b).get_opcodes()
	return parse_opcodes(opcodes, a, b)
