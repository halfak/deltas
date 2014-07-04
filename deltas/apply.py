from .operations import Insert, Delete, Equal


def apply(operations, a_tokens, b_tokens):
    
    for operation in operations:
        
        if isinstance(operation, Equal):
            #print("Equal: {0}".format(str(a_tokens[operation.a1:operation.a2])))
            yield from a_tokens[operation.a1:operation.a2]
        
        elif isinstance(operation, Insert):
            #print("Insert: {0}".format(str(b_tokens[operation.b1:operation.b2])))
            yield from b_tokens[operation.b1:operation.b2]
        
        elif isinstance(operation, Delete):
            #print("Delete: {0}".format(str(a_tokens[operation.a1:operation.a2])))
            pass
        
        else:
            raise TypeError("Unexpected operation type " + \
                            "{0}".format(type(operation)))
