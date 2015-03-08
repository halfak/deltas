import yamlconf
"""
"""

class Engine:
    """
    Constructs a diff engine.
    """

    class Processor:
        """
        Constructs a new diff processor for processing many versions
        of a single text.
        """

        def process(text):
            raise NotImplementedError()


    def processor():
        """
        Configures and returns a new :class:`deltas.algorithms.Engine.Processor`
        """
        raise NotImplementedError()

    @classmethod
    def from_config(cls, config, name, section_key="engines"):
        """
        Constructs a :class:`deltas.algorithms.Engine` from a configuration
        doc.
        """
        section = config[section_key][name]
        if 'module' in section:
            return yamlconf.import_module(section['module'])
        else:
            Engine = yamlconf.import_module(section['class'])
            return Engine.from_config(config, name, section_key=section_key)
