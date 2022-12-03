from itertools import tee
from functools import reduce
from more_itertools import chunked


def priority(item):
    if item.isupper():
        return ord(item) - ord('A') + 27
    else:
        return ord(item) - ord('a') + 1


def intersect_two_halves(rucksack):
    half_point = len(rucksack) // 2
    return set(rucksack[:half_point]) & (set(rucksack[half_point:]))


with open('input.txt', 'r') as file:
    rucksacks = tee((line.strip('\n') for line in file), 2)
    # PART ONE
    print(sum((priority(intersect_two_halves(rucksack).pop())
               for rucksack in rucksacks[0])))

    # PART TWO
    print(sum(map(lambda group: priority(reduce(lambda x, y: x & y, group).pop()),
                  chunked((set(rucksack) for rucksack in rucksacks[1]), 3))))
