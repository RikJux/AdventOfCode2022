import numpy as np
from operator import itemgetter


def visible_from_left(trees_line):
    is_visible = np.full(trees_line.shape[1], False)
    while True:
        highest_tree_idx = max(np.ndenumerate(trees_line), key=itemgetter(1))[0][1]
        trees_line = trees_line[:, :highest_tree_idx]
        is_visible[highest_tree_idx] = True
        if highest_tree_idx == 0:
            break
    return is_visible


def visible_from_right(trees_line):
    return np.flip(visible_from_left(np.flip(trees_line)))


def visible_from_up(trees_line):
    return visible_from_left(np.reshape(trees_line, -1))


def visible_from_down(trees_line):
    return np.flip(visible_from_up(np.flip(trees_line)))
