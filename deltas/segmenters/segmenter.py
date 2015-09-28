import yamlconf


class Segmenter:
    """
    Constructs a token segmentation strategy.
    """
    def __init__(self):
        pass

    def segment(self, tokens):
        """
        Segments a sequence of :class:`~deltas.Token` into a
        `iterable` of :class:`~deltas.Segment`
        """
        raise NotImplementedError()

    @classmethod
    def from_config(cls, config, name, section_key="segmenters"):
        """
        Constructs a segmenter from a configuration doc.
        """
        section = config[section_key][name]
        segmenter_class_path = section['class']
        Segmenter = yamlconf.import_module(segmenter_class_path)
        return Segmenter.from_config(config, name, section_key=section_key)
