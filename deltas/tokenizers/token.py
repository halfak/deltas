"""
Tokens represent chuncks of text that have semantic meaning.  A Token class that
extends :class:`str` is profivided.

.. autoclass:: deltas.tokenizers.Token
    :members:
"""


class Token(str):

    __slots__ = ("type", "i", "start", "end")

    @classmethod
    def construct(cls, content, i, type=None):
        t = cls(content)
        t.i = i
        t.type = type
        t.start = i
        t.end = i+1
        return t

'''
    def __new__(cls, content, *args, **kwargs):
        if isinstance(content, cls):
            return content
        else:
            return super().__new__(cls, content)

    def __init__(self, content, i, type=None):
        super().__init__()
        self.type = str(type) if type is not None else None
        self.i = int(i)

    def __str__(self):
        return super().__str__()

    def __repr__(self):
        return "{0}({1}, i={2}, type={3})" \
               .format(self.__class__.__name__,
                       super().__repr__(),
                       self.i,
                       repr(self.type))

    @property
    def start(self):
        return self.i

    @property
    def end(self):
        return self.i+1
'''
