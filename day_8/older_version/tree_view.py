import numpy as np


def right_view(trees_line):
    tot_visibility = np.full(trees_line.shape[1], 0)
    for (_, idx), tree in np.ndenumerate(trees_line):
        right_trees = trees_line[:, (idx + 1):]
        while right_trees.size > 0:
            tot_visibility[idx] += 1
            head = right_trees[:, 0][0]
            if head >= tree:
                break
            right_trees = right_trees[:, 1:]
    return tot_visibility


def left_view(trees_line):
    return np.flip(right_view(np.flip(trees_line)))


def down_view(trees_line):
    return right_view(np.reshape(trees_line, -1))


def up_view(trees_line):
    return np.flip(down_view(np.flip(trees_line)))
