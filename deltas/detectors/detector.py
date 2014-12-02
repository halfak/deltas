import yamlconf


class Detector:
    
    def diff(a, b): raise NotImplementedError()
    
    @classmethod
    def from_config(cls, doc, name):
        detector_class_path = doc['detectors'][name]['class']
        Detector = yamlconf.import_module(detector_class_path)
        return Detector.from_config(doc, name)
