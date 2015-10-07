"""
Performs a diffs using a tree of matchable segments in order to remain robust
to content moves.  This module supports the use of a custom
:class:`~deltas.Segmenter`.

.. autofunction:: deltas.algorithms.segment_matcher.diff

.. autofunction:: deltas.algorithms.segment_matcher.diff_segments

.. autofunction:: deltas.algorithms.segment_matcher.process

.. autoclass:: deltas.SegmentMatcher
    :members:
"""
from collections import defaultdict

from . import sequence_matcher
from ..operations import Delete, Equal, Insert
from ..segmenters import (MatchableSegment, ParagraphsSentencesAndWhitespace,
                          Segment, Segmenter)
from ..tokenizers import Token, Tokenizer, text_split
from .diff_engine import DiffEngine

SEGMENTER = ParagraphsSentencesAndWhitespace()
TOKENIZER = text_split


def diff(a, b, segmenter=None):
    """
    Performs a diff comparison between two sequences of tokens (`a` and `b`)
    using `segmenter` to cluster and match
    :class:`deltas.MatchableSegment`.

    :Example:
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
        insert '' '  '
        equal 'This is some text.' 'This is some text.'
        delete '  ' ''

    :Parameters:
        a : `list`(:class:`deltas.tokenizers.Token`)
            Initial sequence
        b : `list`(:class:`deltas.tokenizers.Token`)
            Changed sequence
        segmenter : :class:`deltas.Segmenter`
            A segmenter to use on the tokens.

    :Returns:
        An `iterable` of operations.
    """
    a, b = list(a), list(b)
    segmenter = segmenter or SEGMENTER

    # Cluster the input tokens
    a_segments = segmenter.segment(a)
    b_segments = segmenter.segment(b)

    return diff_segments(a_segments, b_segments)


def diff_segments(a_segments, b_segments):
    """
    Performs a diff comparison between two pre-clustered
    :class:`deltas.Segment` trees.  In most cases, segmentation
    takes 100X more time than actually performing the diff.

    :Parameters:
        a_segments : :class:`deltas.Segment`
            An initial sequence
        b_segments : :class:`deltas.Segment`
            A changed sequence

    :Returns:
        An `iterable` of operations.
    """
    # Match and re-sequence unmatched tokens
    a_segment_tokens, b_segment_tokens = _cluster_matching_segments(a_segments,
                                                                    b_segments)

    # Perform a simple LCS over unmatched tokens and clusters
    clustered_ops = sequence_matcher.diff(a_segment_tokens, b_segment_tokens)

    # Return the expanded (de-clustered) operations
    return (op for op in SegmentOperationsExpander(clustered_ops,
                                                   a_segment_tokens,
                                                   b_segment_tokens).expand())


def process(texts, *args, **kwargs):
    """
    Processes a single sequence of texts with a
    :class:`~deltas.SegmentMatcher`.

    :Parameters:
        texts : `iterable`(`str`)
            sequence of texts
        args : `tuple`
            passed to :class:`~deltas.SegmentMatcher`'s
            constructor
        kwaths : `dict`
            passed to :class:`~deltas.SegmentMatcher`'s
            constructor
    """
    processor = SegmentMatcher.Processor(*args, **kwargs)
    for text in texts:
        yield processor.process(text)


class SegmentMatcher(DiffEngine):
    """
    Constructs a segment matcher diff engine that preserves segmentation state
    and is able to process changes sequentially.  When detecting changes
    across many versions of a text this strategy will be about twice as fast as
    calling :func:`diff` sequentially.

    :Example:
        >>> from deltas import SegmentMatcher
        >>> from deltas import text_split
        >>>
        >>> engine = SegmentMatcher(text_split)
        >>>
        >>> processor = engine.processor()
        >>> ops, a, b = processor.process("This is a version.  It has some " +
        ...                               "text in it.")
        >>> print(" ".join(repr(''.join(b[op.b1:op.b2])) for op in ops))
        'This is a version.  It has some text in it.'
        >>> ops, a, b = processor.process("This is a version.  However, it " +
        ...                               "has different.")
        >>> print(" ".join(repr(''.join(b[op.b1:op.b2])) for op in ops))
        'This is a version.  ' '' 'However, it' ' has ' '' 'different' '.'
        >>> ops, a, b = processor.process("Switching it up here.  This is a " +
        ...                               "version.")
        >>> print(" ".join(repr(''.join(b[op.b1:op.b2])) for op in ops))
        '' 'Switching' ' it ' '' 'up' ' ' '' 'here' '.' '  ' 'This is a version.'
    """  # noqa

    class Processor(DiffEngine.Processor):
        """
        A processor used by the SegmentMatcher difference engine to track the
        history of a single text.
        """
        def __init__(self, tokenizer=None, segmenter=None, last_text=None,
                           last_tokens=None, last_segments=None):
            self.tokenizer = tokenizer or TOKENIZER
            self.segmenter = segmenter or SEGMENTER
            self.update(last_text, last_tokens, last_segments)

        def update(self, last_text=None, last_tokens=None, last_segments=None):
            if last_segments is not None:
                self.last_segments = last_segments
                self.last_tokens = self.last_segments.tokens()
            elif last_tokens is not None:
                self.last_tokens = last_tokens
                self.last_segments = self.segmenter.segment(last_tokens)
            elif last_text is not None:
                self.last_tokens = self.tokenizer.tokenize(last_text)
                self.last_segments = self.segmenter.segment(self.last_tokens)
            else:
                self.last_tokens = []
                self.last_segments = Segment()

        def process(self, text, token_class=Token):
            """
            Processes a new version of a text and returns the delta.

            :Parameters:
                text : `str`
                    The text to process

            :Returns:
                    A tuple of `operations`, `a_tokens`, `b_tokens`
            """
            # Tokenize and segment
            tokens = self.tokenizer.tokenize(text, token_class=token_class)
            segments = self.segmenter.segment(tokens)

            return self.process_segments(segments, tokens=tokens)

        def process_segments(self, segments, tokens=None):

            if tokens is None:
                tokens = segments.tokens()

            # Perform diff
            _clear_matches(self.last_segments)
            operations = diff_segments(self.last_segments, segments)

            # Update state
            a = self.last_tokens
            b = tokens
            self.last_tokens = tokens
            self.last_segments = segments

            # Return delta
            return operations, a, b


    def __init__(self, tokenizer=None, segmenter=None):
        self.tokenizer = tokenizer or TOKENIZER
        self.segmenter = segmenter or SEGMENTER

    def processor(self, *args, **kwargs):
        """
        Constructs and configures a processor to process versions of a text.
        """
        return self.Processor(self.tokenizer, self.segmenter, *args, **kwargs)

    def process(self, texts, *args, **kwargs):
        return process(texts, self.tokenizer, self.segmenter, *args, **kwargs)


    @classmethod
    def from_config(cls, config, name, section_key="diff_engines"):
        section = config[section_key][name]
        return cls(
            Tokenizer.from_config(config, section['tokenizer']),
            Segmenter.from_config(config, section['segmenter'])
        )

def _cluster_matching_segments(a_segments, b_segments):

    # Generate a look-up map for matchable segments in 'a'
    a_segment_map = _build_segment_map(a_segments)

    # Find and cluster matching content in 'b'
    b_segment_tokens = list(_match_segments(a_segment_map, b_segments))

    # Expand unmatched segments from 'a'
    a_segment_tokens = list(_expand_unmatched_segments(a_segments))

    return a_segment_tokens, b_segment_tokens

def _build_segment_map(segments):
    d = defaultdict(list)
    for matchable_segment in _get_matchable_segments(segments):
        d[matchable_segment].append(matchable_segment)

    return d

def _get_matchable_segments(segments):
    """
    Performs a depth-first search of the segment tree to get all matchable
    segments.
    """
    for subsegment in segments:
        if isinstance(subsegment, Token):
            break # No tokens allowed next to segments
        if isinstance(subsegment, Segment):
            if isinstance(subsegment, MatchableSegment):
                yield subsegment

            for matchable_subsegment in _get_matchable_segments(subsegment):
                yield matchable_subsegment


def _match_segments(a_segment_map, b_segments):
    for subsegment in b_segments:
        if isinstance(subsegment, Segment):

            if isinstance(subsegment, MatchableSegment) and \
               subsegment in a_segment_map:
                matched_segments = a_segment_map[subsegment]  # Get matches
                for matched_segment in matched_segments:  # For each match
                    matched_segment.match = subsegment  # flag as matched
                subsegment.match = matched_segments[0]  # first match
                yield subsegment  # Dump matched segment

            else:
                for seg_or_tok in _match_segments(a_segment_map, subsegment):
                    yield seg_or_tok  # Recurse

        else:
            yield subsegment  # Dump token


def _expand_unmatched_segments(a_segments):
    for subsegment in a_segments:
        # Check if a segment is matched.
        if isinstance(subsegment, Segment):

            if isinstance(subsegment, MatchableSegment) and \
               subsegment.match is not None:
                yield subsegment # Yield matched segment as cluster
            else:
                for seg_or_tok in _expand_unmatched_segments(subsegment):
                    yield seg_or_tok # Recurse
        else:
            yield subsegment # Dump token


def _clear_matches(segment):
    if isinstance(segment, MatchableSegment):
        segment.match = None

    if isinstance(segment, Segment):
        # Recurse!
        for subsegment in segment:
            _clear_matches(subsegment)

class SegmentOperationsExpander:

    def __init__(self, operations, a_token_segments, b_token_segments):

        self.a_pos = 0
        self.b_pos = 0
        self.a_token_segments = a_token_segments
        self.b_token_segments = b_token_segments
        self.operations = operations

    def expand(self):
        for operation in self.operations:
            if isinstance(operation, Equal):
                #print("Processing equal: {0} {1}".format(self.a_pos, self.b_pos))
                expanded_operations = self._process_equal(operation)
            elif isinstance(operation, Insert):
                #print("Processing insert: {0} {1}".format(self.a_pos, self.b_pos))
                expanded_operations = self._process_insert(operation)
            elif isinstance(operation, Delete):
                #print("Processing remove: {0} {1}".format(self.a_pos, self.b_pos))
                expanded_operations = self._process_delete(operation)
            else:
                assert False, "Should never happen"

            for operation in expanded_operations: yield operation


    def _process_equal(self, op):
        a1 = self.a_pos
        b1 = self.b_pos
        token_len = sum(1 for t_s in self.a_token_segments[op.a1:op.a2]
                          for _ in t_s.tokens())
        self.a_pos += token_len
        self.b_pos += token_len

        yield Equal(a1, self.a_pos, b1, self.b_pos)

    def _process_insert(self, op):
        inserted_token_count = 0

        for t_s in self.b_token_segments[op.b1:op.b2]:
            if isinstance(t_s, Token):
                inserted_token_count += 1
            else: # Found a matched segment
                segment = t_s

                # First, emit an insert for the tokens we have seen so far
                if inserted_token_count > 0:
                    b1 = self.b_pos
                    self.b_pos += inserted_token_count
                    yield Insert(self.a_pos, self.a_pos, b1, self.b_pos)
                    inserted_token_count = 0

                # Now, emit an Equal for the matched segment
                b1 = self.b_pos
                self.b_pos += sum(1 for _ in segment.tokens())
                yield Equal(segment.match.start, segment.match.end,
                            b1, self.b_pos)



        # Cleanup!  Make sure we emit any remaining inserted tokens.
        if inserted_token_count > 0:
            b1 = self.b_pos
            self.b_pos += inserted_token_count
            yield Insert(self.a_pos, self.a_pos, b1, self.b_pos)
            inserted_token_count = 0

    def _process_delete(self, op):
        removed_token_count = 0
        for t_s in self.a_token_segments[op.a1:op.a2]:

            if isinstance(t_s, Token):
                removed_token_count += 1
            else: # Found a matched token... not removed -- just moved
                segment = t_s

                if removed_token_count > 0:
                    a1 = self.a_pos
                    self.a_pos += removed_token_count
                    yield Delete(a1, self.a_pos, self.b_pos, self.b_pos)
                    removed_token_count = 0

                # update & reset!
                self.a_pos += sum(1 for _ in segment.tokens())

        # cleanup
        if removed_token_count > 0:
            a1 = self.a_pos
            self.a_pos += removed_token_count
            yield Delete(a1, self.a_pos, self.b_pos, self.b_pos)
