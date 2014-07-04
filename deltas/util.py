from nose.tools import eq_

from .tokenizers import TextSplit
from .apply import apply


def test_diff_and_replay(diff, tokenizer=None):
    a = """
    This sentence is going to get copied. This sentence is going to go away.
    
    ASDSJDNA  asas random words
    
    This is another sentence.
    """
    
    b = """
    This sentence is going to get copied.  Wha... a new thing appeared!
    
    ASDSJDNA  asas random words
    
    This is another sentence. This sentence is going to get copied.
    """
    tokenizer = tokenizer or TextSplit()
    a_tokens = tokenizer.tokenize(a)
    b_tokens = tokenizer.tokenize(b)
    operations = list(diff(a_tokens, b_tokens))
    
    replay_b = "".join(
        str(t) for t in apply(operations, a_tokens, b_tokens)
    )
    eq_(b, replay_b)


class LookAhead:
    
    class DONE: pass
    
    def __new__(cls, it):
        if isinstance(it, cls):
            return it
        elif hasattr(it, "__next__") or hasattr(it, "__iter__"):
            return cls.from_iterable(it)
        else:
            raise TypeError("Expected iterable, got {0}", type(it))
    
    @classmethod
    def from_iterable(cls, iterable):
        instance = super().__new__(cls)
        instance.initialize(iterable)
        return instance
    
    def __init__(self, *args, **kwargs): pass
    
    def initialize(self, iterable):
        self.iterable = iter(iterable)
        self.i = -1 # Will increment to zero in a moment
        self._load_next()
        
    def _load_next(self):
        try:
            self.next = next(self.iterable)
            self.i += 1
        except StopIteration:
            self.next = self.DONE
    
    def __iter__(self): return self
    
    def __next__(self):
        if self.empty():
            raise StopIteration()
        else:
            current = self.next
            self._load_next()
            return current
    
    def pop(self):
        return self.__next__()
    
    def peek(self):
        return self.next
    
    def empty(self):
        return self.next == self.DONE
