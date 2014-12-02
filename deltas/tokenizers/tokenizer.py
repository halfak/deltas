import yamlconf


class Tokenizer:
    """
    An abstract class representing the tokenizer interfact.
    """
    def tokenize(self, text): raise NotImplementedError()
    
    @classmethod
    def from_config(cls, doc, name):
        tokenizer_class_path = doc['tokenizers'][name]['class']
        Tokenizer = yamlconf.import_module(tokenizer_class_path)
        return Tokenizer.from_config(doc, name)
