from deltas import segment_matcher, text_split
from deltas import apply_get_a, apply_get_b
from deltas import Operation, Insert, Delete, Equal

import deltas
from pprint import pprint

a = text_split.tokenize("This is some text.  This is some other text.")
b = text_split.tokenize("This is some other text.  This is some text.")
operations = segment_matcher.diff(a, b)

operations_format = []
for op in operations:
    tmp = {
        'name': op.name,
        'a1': op.a1,
        'b1': op.b1,
        'a2': op.a2,
        'b2': op.b2,
        'tokens' : [str(token) for token in op.relevant_tokens(a,b)]
    }
    operations_format.append(tmp)

print(apply_get_a(operations_format))
print(apply_get_b(operations_format))

operations_new = []
for op in operations_format:
    tmp = Operation(name = op["name"], a1 = op["a1"], a2 = op["a2"], b1 = op["b1"], b2 = op["b2"])
    operations_new.append(tmp)

print(operations)
print(operations_new)
