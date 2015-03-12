from nose.tools import eq_

from ..apply import apply
from ..tokenizers import text_split


def diff_and_replay(diff, tokenizer=None):
    a = """
    This sentence is going to get copied. This sentence is going to go away.

    This is a paragraph that is mostly going to change.  However, there's going
    to be a sentence right in the middle that stays.  And now we're done with
    that.

    This is another sentence. asldknasl dsal dals dals dlasd oa kdlawbndkubawdk
    """

    b = """
    This sentence is going to get copied.  Wha... a new thing appeared!

    Everyone thought that this paragraph would totally change.  However, there's
    going to be a sentence right in the middle that stays.  Isn't that funny!?

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
    eq_(b, ''.join(replay_b))


    a = "I'm new here.  This sentence is a sentence. I'm new here."
    b = "I'm new here. Sentence is a sentence."

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
    eq_(b, ''.join(replay_b))
