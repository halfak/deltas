def apply_get_b(operations_diff_file):

    length_b = max([operation["b2"] for operation in operations_diff_file])
    b = [''] * length_b

    for operation in operations_diff_file:

        if operation["name"] == "equal" or operation["name"] == "insert":
            #print("Equal: {0}".format(str(a_tokens[operation.a1:operation.a2])))
            if "tokens" in operation.keys():
                b[operation["b1"]:operation["b2"]] = operation["tokens"]

        elif operation["name"] == "delete":
            #print("Insert: {0}".format(str(b_tokens[operation.b1:operation.b2])))
            pass

        else:
            raise TypeError("Unexpected operation type " + \
                            "{0}".format(type(operation)))

    return ' '.join(b)
