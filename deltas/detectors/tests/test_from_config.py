from nose.tools import eq_

from ...tokenizers import wikitext_split
from ..detector import Detector


def test_from_config():
    doc = {
        'detectors': {
            'segment_matcher':{
                'class': "deltas.detectors.SegmentMatcher",
                'segmenter': "western_psw"
            }
        },
        'segmenters': {
            'western_psw': {
                'class': "deltas.segmenters.ParagraphsSentencesAndWhitespace"
            }
        }
    }
    
    segment_matcher = Detector.from_config(doc, "segment_matcher")
    
    operations = segment_matcher.diff(wikitext_split.tokenize("Foo bar."),
                                      wikitext_split.tokenize("Foo burp."))
    
    eq_(len(list(operations)), 4)
