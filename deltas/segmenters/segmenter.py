import yamlconf


class Segmenter:
    
    def __init__(self): pass
    
    def segment(self, text): raise NotImplementedError()
    
    @classmethod
    def from_config(cls, doc, name):
        segmenter_class_path = doc['segmenters'][name]['class']
        Segmenter = yamlconf.import_module(segmenter_class_path)
        return Segmenter.from_config(doc, name)
