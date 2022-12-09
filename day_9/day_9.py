from numpy import sign
from itertools import repeat, chain, accumulate

move_dict = {'U': (0, 1), 'D': (0, -1), 'L': (-1, 0), 'R': (1, 0)}


def move(pos, movement):
    return tuple(t + m for t, m in zip(pos, movement))


def knot_move(head_pos, knot_pos):
    head_rel_pos = tuple(h - t for h, t in zip(head_pos, knot_pos))
    ((low_idx, low_coord), (high_idx, high_coord)) = sorted(enumerate(head_rel_pos), key=lambda x: abs(x[1]))
    movement = [0, 0]
    if abs(high_coord) == 2:
        if abs(low_coord) >= 1:
            movement[low_idx] = sign(low_coord)
        movement[high_idx] = sign(high_coord)
        knot_pos = move(knot_pos, movement)

    return knot_pos


def knot_all_moves(positions, k_pos=(0, 0)):
    knot_positions = list()
    for curr_H_pos in positions:
        k_pos = knot_move(curr_H_pos, k_pos)
        knot_positions.append(k_pos)
    return knot_positions


def single_movements(command):
    """Unpack a command into single movements"""
    direction, amount = move_dict[command[0]], int(command[1])
    return repeat(direction, amount)


with open('input.txt', 'r') as file:
    commands = (chain.from_iterable((single_movements(tuple(line.strip("\n").split(" "))) for line in file)))
    head_positions = list(accumulate(commands, func=move, initial=(0, 0)))

# PART ONE
print(len(set(knot_all_moves(head_positions))))

# PART TWO
n_knots = 9
for n_knots in range(9):
    head_positions = knot_all_moves(head_positions)

print(len(set(head_positions)))
