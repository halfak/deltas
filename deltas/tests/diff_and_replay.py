from nose.tools import eq_

from ..apply import apply
from ..tokenizers import text_split


def diff_and_replay(diff, tokenizer=None):
    a = """
    This sentence is going to get copied. This sentence is going to go away.
    
    ASDSJDNA  asas random words.
    
    This is another sentence.
    """
    
    b = """
    This sentence is going to get copied.  Wha... a new thing appeared!
    
    ASDSJDNA  asas random words.
    
    This is another sentence. This sentence is going to get copied.
    """
    a_tokens = list(text_split.tokenize(a))
    b_tokens = list(text_split.tokenize(b))
    operations = list(diff(a_tokens, b_tokens))
    
    for op in operations:
        if op.name == "equal":
            print("equal: " + str(a_tokens[op.a1:op.a2]))
        elif op.name == "delete":
            print("delete: " + str(a_tokens[op.a1:op.a2]))
        elif op.name == "insert":
            print("insert: " + str(b_tokens[op.b1:op.b2]))
    
    replay_b = [str(t) for t in apply(operations, a_tokens, b_tokens)]
    eq_(b_tokens, replay_b)
