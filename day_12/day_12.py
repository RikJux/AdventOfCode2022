from more_itertools import map_if, flatten
from functools import partial
from collections import deque
from itertools import cycle
from operator import itemgetter


def transpose(iterator):
    return zip(*iterator)


def backwards(iterator):
    return map(lambda line: reversed(list(line)), iterator)


def get_source_and_dest(grid):
    s_pos = None
    e_pos = None
    for row_idx, line in enumerate(grid):
        for col_idx, square in enumerate(line):
            if square == 'S':
                s_pos = (row_idx, col_idx)
            elif square == 'E':
                e_pos = (row_idx, col_idx)
            if s_pos and e_pos:
                return {'S': s_pos, 'E': e_pos}


def can_move(line, direction):
    line = list(line)
    pairwise_line = zip(line, line[1:])
    return [direction if (second <= first or second == first + 1)
            else (0, 0) for first, second in pairwise_line] + [(0, 0)]


can_move_left = partial(can_move, direction=(0, -1))
can_move_right = partial(can_move, direction=(0, 1))
can_move_down = partial(can_move, direction=(-1, 0))
can_move_up = partial(can_move, direction=(1, 0))


def fill_paths(start_x, start_y, possible_directions):
    max_size_path = len(possible_directions[0]) * len(possible_directions)

    shortest_paths = [[max_size_path] * len(possible_directions[0]) for _ in range(len(possible_directions))]
    visited = [[False] * len(possible_directions[0]) for _ in range(len(possible_directions))]
    to_explore = deque([(start_x, start_y, 0)])

    while True:
        if len(to_explore) == 0:
            break

        current = to_explore.pop()
        curr_x, curr_y, curr_dist = current

        shortest_paths[curr_x][curr_y] = curr_dist

        siblings = [tuple(c + d for c, d in zip(current, direction)) for direction in
                    possible_directions[curr_x][curr_y]]
        for sib_x, sib_y in siblings:
            if not visited[sib_x][sib_y]:  # not yet visited
                visited[sib_x][sib_y] = True
                to_explore.appendleft((sib_x, sib_y, curr_dist + 1))

    return shortest_paths


with open("input.txt", "r") as file:
    heightmap = [(list(line.strip("\n"))) for line in file]
    s_d_dict = get_source_and_dest(heightmap)
    heightmap = list(map(lambda line: list(map_if(line,
                                                  lambda x: x != 'S' and x != 'E',
                                                  lambda x: ord(x) - ord('a'),
                                                  lambda x: -1 if x == 'S' else ord('z') - ord('a'))), heightmap))

left_to_right = map(can_move_right, heightmap)
right_to_left = backwards(map(can_move_left, backwards(heightmap)))
down_to_up = transpose(map(can_move_up, transpose(heightmap)))
up_to_down = transpose(backwards(map(can_move_down, backwards(transpose(heightmap)))))

directions = map(lambda lines: zip(*lines), zip(left_to_right, right_to_left, up_to_down, down_to_up))
directions = list(map(list, directions))


# PART ONE
print(fill_paths(*s_d_dict['S'], directions)[s_d_dict['E'][0]][s_d_dict['E'][1]])

# PART TWO TODO change the fill_paths algorithm
low_points = flatten(map(lambda line: zip(cycle([line[0]]), map(itemgetter(0), line[1])),
                         enumerate(map(lambda line: filter(lambda sq: sq[1] == 0,
                                                           enumerate(line)), heightmap))))

print(min([fill_paths(*point, directions)[s_d_dict['E'][0]][s_d_dict['E'][1]] for point in low_points]))
