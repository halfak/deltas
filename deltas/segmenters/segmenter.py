import yamlconf


class Segmenter:
    """
    Implements a segmentation strategy
    """
    def __init__(self): pass
    
    def segment(self, tokens):
        """
        Segments a sequence of :class:`~deltas.tokenizers.Token` into a
        sequence of :class:`~deltas.segmenters.Segment`
        """
        raise NotImplementedError()
    
    @classmethod
    def from_config(cls, doc, name):
        segmenter_class_path = doc['segmenters'][name]['class']
        Segmenter = yamlconf.import_module(segmenter_class_path)
        return Segmenter.from_config(doc, name)
