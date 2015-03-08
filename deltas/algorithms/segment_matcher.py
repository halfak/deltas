"""
Match segments
--------------

Performs a diffs using a tree of matchable segments in order to remain robust
to content moves.  This module supports the use of a custom
:class:`~deltas.segmenters.Segmenter`.
"""
from collections import defaultdict

from . import sequence_matcher
from ..operations import Delete, Equal, Insert
from ..segmenters import (MatchableSegment, ParagraphsSentencesAndWhitespace,
                          Segment, Segmenter)
from ..tokenizers import text_split, Token, Tokenizer
from .engine import Engine

SEGMENTER = ParagraphsSentencesAndWhitespace()
"""
The default segmenter.  This segmenter is designed to split western languages
into paragraphs, sentences and whitespace.
"""

TOKENIZER = text_split
"""
The default tokenizer.  This tokenizer preserves all characters and splits up
words, numbers, punctuation and whitespace.
"""

def diff(a, b, segmenter=None):
    """
    Performs a diff comparison between two sequences of tokens (`a` and `b`)
    using `segmenter` to cluster and match
    :class:`deltas.segmenters.MatchableSegment`.

    :Example:
        >>> from deltas import segment_matcher, text_split
        >>>
        >>> a = text_split.tokenize("This is some text.  This is some other text.")
        >>> b = text_split.tokenize("This is some other text.  This is some text.")
        >>> operations = segment_matcher.diff(a, b)
        >>>
        >>> for op in operations:
        ...     print(op.name, repr(''.join(a[op.a1:op.a2])), repr(''.join(b[op.b1:op.b2])))
        ...
        equal 'This is some other text.' 'This is some other text.'
        insert ' ' '  '
        equal 'This is some text.' 'This is some text.'
        delete '  ' ''

    :Parameters:
        a : `list`(:class:`deltas.tokenizers.Token`)
            Initial sequence
        b : `list`(:class:`deltas.tokenizers.Token`)
            Changed sequence
        segmenter : :class:`deltas.segmenters.Segmenter`
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
    :class:`deltas.segmenters.Segment` trees.  In most cases, segmentation
    takes 100X more time than actually performing the diff.

    :Parameters:
        a_segments : :class:`deltas.segmenters.Segment`
            An initial sequence
        b_segments : :class:`deltas.segmenters.Segment`
            A changed sequence

    :Returns:
        An `iterable` of operations.
    """
    a_segments, b_segments = list(a_segments), list(b_segments)

    # Match and re-sequence unmatched tokens
    a_segment_tokens, b_segment_tokens = _cluster_matching_segments(a_segments,
                                                                    b_segments)

    # Perform a simple LCS over unmatched tokens and clusters
    clustered_ops = sequence_matcher.diff(a_segment_tokens, b_segment_tokens)

    # Return the expanded (de-clustered) operations
    return _expand_clustered_ops(clustered_ops,
                                 a_segment_tokens,
                                 b_segment_tokens)



def process(texts, *args, **kwargs):
    processor = SegmentMatcher.Processor(*args, **kwargs)
    for text in texts:
        yield processor.process(text)

class SegmentMatcher(Engine):
    """
    Constructs a segment matcher diff engine that preserves segmentation state
    and is able to process changes sequentially.  When detecting changes
    across many versions of a text this strategy will be about twice as fast as
    calling :func:`diff` sequentially.

    :Example:
        >>> from deltas.algorithms import SegmentMatcher
        >>> from deltas.tokenizers import text_split
        >>>
        >>> engine = SegmentMatcher(text_split)
        >>>
        >>> processor = engine.processor()
        >>> ops, a, b = processor.process("This is a version.  It has some text in it.")
        >>> print(" ".join(repr(''.join(b[op.b1:op.b2])) for op in ops))
        'This is a version.  It has some text in it.'
        >>> ops, a, b = processor.process("This is a version.  However, it has different.")
        >>> print(" ".join(repr(''.join(b[op.b1:op.b2])) for op in ops))
        'This is a version.  ' '' 'However, it' ' has ' '' 'different' '.'
        >>> ops, a, b = processor.process("Switching it up here.  This is a version.")
        >>> print(" ".join(repr(''.join(b[op.b1:op.b2])) for op in ops))
        '' 'Switching' ' it ' '' 'up' ' ' '' 'here' '.' '  ' 'This is a version.'
    """

    class Processor(Engine.Processor):
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
                self.last_segments = self.segments.segment(last_tokens)
            elif last_text is not None:
                self.last_tokens = self.tokenizer.tokenize(last_text)
                self.last_segments = self.segmenter.segment(self.last_tokens)
            else:
                self.last_tokens = []
                self.last_segments = Segment()


        def process(self, text):
            """
            Processes a new version of a text and returns the delta.

            :Parameters:
                text : `str`
                    The text to process

            :Returns:
                A tuple of `operations`, `a_tokens`, `b_tokens`
            """
            # Tokenize and segment
            new_tokens = self.tokenizer.tokenize(text)
            new_segments = self.segmenter.segment(new_tokens)

            # Perform diff
            operations = diff_segments(self.last_segments, new_segments)

            # Update state
            a = self.last_tokens
            b = new_tokens
            self.last_tokens = new_tokens
            self.last_segments = new_segments

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
    def from_config(cls, config, name, section_key="algorithms"):
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

def _expand_clustered_ops(operations, a_token_clusters, b_token_clusters):

    position = 0
    for operation in operations:
        if isinstance(operation, Equal):
            #print("Processing equal:")
            new_ops = _process_equal(position, operation,
                                     a_token_clusters, b_token_clusters)

        elif isinstance(operation, Insert):
            #print("Processing insert:")
            new_ops = _process_insert(position, operation,
                                      a_token_clusters, b_token_clusters)

        elif isinstance(operation, Delete):
            #print("Processing remove:")
            new_ops = _process_delete(position, operation,
                                      a_token_clusters, b_token_clusters)

        else:
            assert False, "Should never happen"

        for new_op in new_ops:

            yield new_op
            position = position + (new_op.b2 - new_op.b1)

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
                matched_segments = a_segment_map[subsegment] # Get matches
                for matched_segment in matched_segments: # For each match
                    matched_segment.match = subsegment # flag as matched
                subsegment.match = matched_segments[0] # Always associate with first match
                yield subsegment # Dump matched segment

            else:
                for seg_or_tok in _match_segments(a_segment_map, subsegment):
                    yield seg_or_tok # Recurse

        else:
            yield subsegment # Dump token


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

def _process_equal(position, operation, a_token_clusters, b_token_clusters):
    yield Equal(a_token_clusters[operation.a1].start,
                a_token_clusters[operation.a2-1].end,
                b_token_clusters[operation.b1].start,
                b_token_clusters[operation.b2-1].end)

def _process_insert(position, operation, a_token_clusters, b_token_clusters):
    inserted_tokens = []
    for token_or_segment in b_token_clusters[operation.b1:operation.b2]:

        if isinstance(token_or_segment, Token):
            inserted_tokens.append(token_or_segment)
        else: # Found a matched token.
            if len(inserted_tokens) > 0:
                yield Insert(inserted_tokens[0].start,
                             inserted_tokens[-1].end,
                             position,
                             position+len(inserted_tokens))

                # update & reset!
                position += len(inserted_tokens)
                inserted_tokens = []

            match = token_or_segment.match
            yield Equal(match.start, match.end,
                        position, position+(match.end-match.start))

            # update!
            position += match.end-match.start



    # cleanup
    if len(inserted_tokens) > 0:
        yield Insert(inserted_tokens[0].start,
                     inserted_tokens[-1].end,
                     position,
                     position+len(inserted_tokens))

def _process_delete(position, operation, a_token_clusters, b_token_clusters):
    removed_tokens = []
    for token_or_segment in a_token_clusters[operation.a1:operation.a2]:

        if isinstance(token_or_segment, Token):
            removed_tokens.append(token_or_segment)
        else: # Found a matched token... not removed -- just moved
            if len(removed_tokens) > 0:
                yield Delete(removed_tokens[0].start,
                             removed_tokens[-1].end,
                             position,
                             position)

            # update & reset!
            position += len(removed_tokens)
            removed_tokens = []

    # cleanup
    if len(removed_tokens) > 0:
        yield Delete(removed_tokens[0].start,
                     removed_tokens[-1].end,
                     position,
                     position)
