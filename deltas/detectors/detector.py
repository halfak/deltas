import yamlconf


class Detector:
    """
    Constructs a delta detector.
    """
    
    def diff(a, b):
        """
        Compares two sequences of tokens and returns an `iterable` of
        :class:`deltas.operations.Operation`.
        """
        raise NotImplementedError()
    
    @classmethod
    def from_config(cls, config, name, section_key="detectors"):
        """
        Constructs a :class:`deltas.detectors.Detector` from a configuration
        doc.
        """
        section = config[section_key][name]
        detector_class_path = section['class']
        Detector = yamlconf.import_module(detector_class_path)
        return Detector.from_config(config, name, section_key=section_key)
