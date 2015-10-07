from .segments import Segment


def print_tree(segment, depth=0):
    if isinstance(segment, Segment):
        print(depth * "\t" + "{0}: '{1}'"\
                             .format(segment.__class__.__name__, str(segment)))
        depth += 1

    for subsegment in segment:
        if isinstance(subsegment, Segment):
            print_tree(subsegment, depth=depth)
