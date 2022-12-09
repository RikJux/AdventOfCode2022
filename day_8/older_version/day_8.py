from itertools import repeat, cycle, starmap
from functools import reduce
from operator import add, mul
from tree_visibility import *
from tree_view import *


def visibility(original_matrix, return_function, reduce_function, all_directions_functions):
    return return_function(reduce(reduce_function,
                                  starmap(np.apply_along_axis,
                                          zip(all_directions_functions,
                                              cycle([1, 0]),
                                              repeat(original_matrix, 4)))))


with open('../input.txt', 'r') as file:
    grid = np.matrix([[int(tree) for tree in line.strip("\n")] for line in file])

# PART ONE: compute how many trees are visible from outside the grid
print(visibility(grid, np.sum, add, [visible_from_left, visible_from_up, visible_from_right, visible_from_down]))

# PART TWO: Compute the highest scenic score possible for any tree
print(visibility(grid, np.max, mul, [right_view, down_view, left_view, up_view]))
