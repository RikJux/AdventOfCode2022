from functools import partial
from copy import deepcopy
from more_itertools import chunked, nth

get_crate = partial(nth, n=1, default=' ')
stacks_part_one = [[] for i in range(9)]


def move_crates(s, n, from_idx, to_idx, function=lambda x: x):
    s[to_idx].extend(function(s[from_idx][-n:]))
    s[from_idx] = s[from_idx][:-n]


with open('input.txt', 'r') as file:
    drawing, procedure = file.read().split(" 1   2   3   4   5   6   7   8   9 \n\n")
    drawing = list(map(lambda level: map(get_crate, chunked(level, 4)), drawing.split("\n")))
    for level in reversed(drawing):  # fill the stacks by initial drawing
        for index, crate in filter(lambda x: x[1] != ' ', enumerate(level)):
            stacks_part_one[index].append(crate)

    stacks_part_two = deepcopy(stacks_part_one)

    procedure = map(lambda move: [int(i) for i in move.split(' ') if i.isdigit()], procedure.split("\n"))
    for move in filter(lambda x: len(x) == 3, procedure):
        n_crates, from_stack_idx, to_stack_idx = move
        from_stack_idx, to_stack_idx = from_stack_idx - 1, to_stack_idx - 1
        # PART ONE: the crane moves a crate at time (so crates have to be appended in reversed order)
        move_crates(stacks_part_one, n_crates, from_stack_idx, to_stack_idx, reversed)
        # PART TWO: the crane moves many crates at time
        move_crates(stacks_part_two, n_crates, from_stack_idx, to_stack_idx)

    print(''.join([stack[-1] for stack in stacks_part_one]))
    print(''.join([stack[-1] for stack in stacks_part_two]))
