class Segmenter:
    
    def __init__(self): pass
    
    def segment(self, text): raise NotImplementedError()
    
    @classmethod
    def from_config(cls, doc, name): raise NotImplementedError()
