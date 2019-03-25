from pprint import pprint

def apply_get_a(operations_diff_file):

    try:
        length_a = max([operation["a2"] for operation in operations_diff_file])
        a = [''] * length_a

        for operation in operations_diff_file:

            if operation["name"] == "equal" or operation["name"] == "delete":
                #print("Equal: {0}".format(str(a_tokens[operation.a1:operation.a2])))
                if "tokens" in operation.keys():
                    a[operation["a1"]:operation["a2"]] = operation["tokens"]

            elif operation["name"] == "insert":
                #print("Insert: {0}".format(str(b_tokens[operation.b1:operation.b2])))
                pass

            else:
                raise TypeError("Unexpected operation type " + \
                                "{0}".format(type(operation)))

        return ' '.join(a)
    except:
        pprint(operations_diff_file)
