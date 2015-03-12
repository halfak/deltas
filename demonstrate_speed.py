import cProfile as profile
import random
import time
import pickle

from deltas import segment_matcher, sequence_matcher
from deltas.segmenters import ParagraphsSentencesAndWhitespace
from deltas.tokenizers import wikitext_split
from mw import api

tokenizer = wikitext_split
segmenter = ParagraphsSentencesAndWhitespace()

session = api.Session("https://en.wikipedia.org/w/api.php")
common1 = session.revisions.get(638029546, properties={"content"})['*']
common2 = session.revisions.get(638077284, properties={"content"})['*']

common1_tokens = list(tokenizer.tokenize(common1))
common2_tokens = list(tokenizer.tokenize(common2))

words = [l.strip() for l in open('/usr/share/dict/words')]
random1 = ''.join(random.choice(words) if t.type == "word" else str(t)
                  for t in common1_tokens)
random2 = ''.join(random.choice(words) if t.type == "word" else str(t)
                  for t in common1_tokens)

random2_tokens = list(tokenizer.tokenize(random2))
random1_tokens = list(tokenizer.tokenize(random1))

print("Tokenizing:")
def tokenize_common():
    start = time.time()
    for _ in range(25):
        tokens = list(tokenizer.tokenize(common1))
    print("\tcommon: {0}".format((time.time() - start)/25))
tokenize_common()
#profile.run('segment_common()', sort="cumulative")

print("Pickling segments:")
def segments_pickle():
    segments = segmenter.segment(common1_tokens)
    pickled_segments = pickle.dumps(segments)
    start = time.time()
    for _ in range(25):
        pickled_segments = pickle.dumps(segments)
    print("\tpickling: {0}".format((time.time() - start)/25))
    for _ in range(25):
        unpickled_segments = pickle.loads(pickled_segments)
    print("\tunpickling: {0}".format((time.time() - start)/25))
segments_pickle()
#profile.run('segment_common()', sort="cumulative")

print("Running sequence matcher (LCS):")
def sequence_common():
    start = time.time()
    for _ in range(25):
        operations = list(sequence_matcher.diff(common1_tokens, common2_tokens))
    print("\tcommon: {0}".format((time.time() - start)/25))
sequence_common()
#profile.run('sequence_common()', sort="cumulative")

def sequence_random():
    start = time.time()
    for _ in range(25):
        operations = list(sequence_matcher.diff(random1_tokens, random2_tokens))
    print("\trandom: {0}".format((time.time() - start)/25))
#sequence_random()
#profile.run('sequence_random()', sort="cumulative")

print("Segmenting:")
def segment_common():
    start = time.time()
    for _ in range(25):
        segments = list(segmenter.segment(common1_tokens))
    print("\tcommon: {0}".format((time.time() - start)/25))
segment_common()
#profile.run('segment_common()', sort="cumulative")

print("Running segment matcher:")
def segment_common():
    start = time.time()
    for _ in range(25):
        operations = list(segment_matcher.diff(common1_tokens, common2_tokens))
    print("\tcommon: {0}".format((time.time() - start)/25))
segment_common()
#profile.run('segment_common()', sort="cumulative")
def segment_common_fast():
    start = time.time()
    sm = segment_matcher.SegmentMatcher()
    processor = sm.processor()
    for _ in range(25):
        operations = list(processor.process(common1))
        operations = list(processor.process(common2))
    print("\tcommon_fast: {0}".format((time.time() - start)/50))
segment_common_fast()
#profile.run('segment_common()', sort="cumulative")

def segment_random():
    start = time.time()
    for _ in range(25):
        operations = list(segment_matcher.diff(random1_tokens, random2_tokens))
    print("\trandom: {0}".format((time.time() - start)/25))
#segment_random()
#profile.run('segment_random()', sort="cumulative")

common1_segments = segmenter.segment(common1_tokens)
common2_segments = segmenter.segment(common2_tokens)
random1_segments = segmenter.segment(random1_tokens)
random2_segments = segmenter.segment(random2_tokens)

print("Running segment matcher (post segmentation):")
def segment_common_seg():
    start = time.time()
    for _ in range(25):
        operations = list(segment_matcher.diff_segments(common1_segments, common2_segments))
    print("\tcommon: {0}".format((time.time() - start)/25))
segment_common_seg()
#profile.run('segment_common_seg()', sort="cumulative")

def segment_random_seg():
    start = time.time()
    for _ in range(25):
        operations = list(segment_matcher.diff_segments(random1_segments, random2_segments))
    print("\trandom: {0}".format((time.time() - start)/25))
#segment_random_seg()
#profile.run('segment_random()', sort="cumulative")
