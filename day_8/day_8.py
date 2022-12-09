from itertools import tee, chain
from functools import reduce
from operator import itemgetter, add, mul


def visible_from_left(tree_line):
    is_visible = [False] * len(tree_line)
    while True:
        highest_tree_idx = max(enumerate(tree_line), key=itemgetter(1))[0]
        tree_line = tree_line[:highest_tree_idx]
        is_visible[highest_tree_idx] = True
        if highest_tree_idx == 0:
            break

    return is_visible


def view_to_right(tree_line):
    tot_visibility = [0] * len(tree_line)
    for idx, tree in enumerate(tree_line):
        trees_on_the_right = tree_line[idx + 1:]
        while len(trees_on_the_right) > 0:
            tot_visibility[idx] += 1
            head = trees_on_the_right[0]
            if head >= tree:
                break
            trees_on_the_right = trees_on_the_right[1:]

    return tot_visibility


def visibility(trees, visibility_function, aggregate_function, reduce_function):
    tree_lines = tee(trees, 4)
    # create iterator over the trees' matrix, each has a view from a different side
    left_to_right = map(visibility_function, tree_lines[0])
    right_to_left = map(lambda x: visibility_function(list(reversed(x))), tree_lines[1])
    up_to_down = map(lambda x: visibility_function(list(x)), zip(*tree_lines[2]))
    down_to_up = map(lambda x: visibility_function(list(reversed(x))), zip(*tree_lines[3]))

    # put elements back in the proper order (left to right, up to down) to aggregate results
    right_to_left = map(lambda x: list(reversed(x)), right_to_left)
    up_to_down = map(list, zip(*up_to_down))
    down_to_up = map(list, reversed(list(zip(*down_to_up))))

    return reduce(reduce_function,
                  chain.from_iterable(map(lambda x: list(map(aggregate_function, zip(*x))),
                                          zip(left_to_right, right_to_left, up_to_down, down_to_up))))


with open('input.txt', 'r') as file:
    forest = tee(([int(tree) for tree in line.strip("\n")] for line in file), 2)

    # PART ONE
    print(visibility(forest[0], visible_from_left, any, add))

    # PART TWO
    print(visibility(forest[1], view_to_right, lambda y: reduce(mul, y), max))
    