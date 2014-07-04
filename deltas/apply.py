from ..types import Insert, Persist, Remove


def apply(operations, a_tokens):
    
    for operation in operations:
        
        if isinstance(operation, Persist):
            yield from a_tokens[operation.start:operation.end]
        
        elif isinstance(operation, Insert):
            yield from operation.tokens
        
        elif isinstance(operation, Remove):
            pass
        
        else:
            raise TypeError("Unexpected operation type " + \
                            "{0}".format(type(operation)))
