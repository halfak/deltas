from nose.tools import eq_

from ...apply import apply
from ...operations import Delete, Equal, Insert
from ...tests.diff_and_replay import diff_and_replay
from ...tests.diff_sequence import diff_sequence
from ...tokenizers import text_split, wikitext_split
from ..segment_matcher import diff, process


def test_diff_and_replay():
    return diff_and_replay(diff)


def test_engine():
    return diff_sequence(process)


def test_easy_diff():
    a = "Apples are red."
    b = "Apples are tasty and red."

    operation_tokens = process([a, b], tokenizer=wikitext_split)

    # Apples are red.
    operations, a, b = next(operation_tokens)

    # Apples are tasty and red.
    operations, a, b = next(operation_tokens)

    eq_(
        list(operations),
        [
            Equal(0, 4, 0, 4),
            Insert(4, 4, 4, 8),
            Equal(4, 6, 8, 10)
        ]
    )
