class Tokenizer:
    """
    An abstract class representing the tokenizer interfact.
    """
    def tokenize(self, text):
        """
        Extend this class for a custom tokenizer.
        """
        raise NotImplementedError()
    
    @classmethod
    def from_config(cls, doc, name):
        raise NotImplementedError()
