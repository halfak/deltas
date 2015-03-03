

class Token(str):
    
    __slots__ = ("type", "i")
    
    def __new__(cls, *args, **kwargs):
        if len(args) == 1 and len(kwargs) == 0:
            if isinstance(args[0], cls):
                return args[0]
            else:
                raise TypeError("Expected {0}, got {1}".format(cls,
                                                               type(args[0])))
                
        else:
            inst = super().__new__(cls, args[0])
            inst.initialize(*args, **kwargs)
            return inst
    
    def __init__(self, *args, **kwargs): pass
    
    def initialize(self, content, i, type=None):
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
