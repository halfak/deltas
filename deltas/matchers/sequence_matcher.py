"""
A simple wrapper around :class:`difflib.SequenceMatcher` that confirms to the
:func:`diff` API.

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
	opcodes = SM(None, a, b).get_opcodes()
	return parse_opcodes(opcodes)
