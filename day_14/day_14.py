from numpy import sign
from sortedcontainers import SortedSet
from collections import defaultdict
from operator import itemgetter
from copy import deepcopy

rock_dict = defaultdict(lambda: SortedSet())


def rocks(iterator):
    for pattern in iterator:
        prev = None
        for rock in pattern:
            current = rock
            if prev:
                direction = tuple(sign(c - p) for c, p in zip(current, prev))
                while prev != current:
                    prev = tuple(p + d for p, d in zip(prev, direction))
                    yield prev
            else:
                yield current
            prev = current


def pour_sand(rock_map, break_on_floor=False, start=(500, 0), floor_step=2):
    obstacles = deepcopy(rock_map)
    current = start
    sand = 0
    floor = max(map(itemgetter(-1), obstacles.values()), key=itemgetter(1))[1] + floor_step

    while True:
        try:
            first_obstacle = obstacles[current[0]][obstacles[current[0]].bisect_left(current)]
            if first_obstacle == start:
                break
            landing = tuple(lnd + d for lnd, d in
                            zip(first_obstacle, (0, -1)))
        except IndexError:  # the grain would fall in the void
            if break_on_floor:
                break
            landing = (current[0], floor - 1)
        left = tuple(lnd + d for lnd, d in zip(landing, (-1, 1)))
        if left not in obstacles[left[0]] and left[1] < floor:  # move on left diagonal
            current = left
        else:
            right = tuple(lnd + d for lnd, d in zip(landing, (1, 1)))
            if right not in obstacles[right[0]] and right[1] < floor:  # move on right diagonal
                current = right
            else:  # cannot move anymore
                sand += 1
                obstacles[current[0]].add(landing)
                current = start

    return sand


with open('input.txt', 'r') as file:
    for col, row in rocks((map(lambda t: tuple(map(int, t.split(','))), line.strip('\n').split(" -> ")))
                          for line in file):
        rock_dict[col].add((col, row))

# PART ONE
print(pour_sand(rock_dict, True))
# PART TWO
print(pour_sand(rock_dict))
