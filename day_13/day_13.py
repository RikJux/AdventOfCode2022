from itertools import chain
from collections import Counter


def recursive_compare(left, right):
    if isinstance(left, int) and isinstance(right, int):
        return -1 if left < right else 1 if right < left else 0
    elif isinstance(left, int) and isinstance(right, list):
        return recursive_compare([left], right)
    elif isinstance(left, list) and isinstance(right, int):
        return recursive_compare(left, [right])
    else:
        if len(left) == 0 and len(right) != 0:
            return -1
        elif len(left) != 0 and len(right) == 0:
            return 1
        elif len(left) == 0 and len(right) == 0:
            return 0
        else:
            first_el_cmp = recursive_compare(left[0], right[0])
            return first_el_cmp if first_el_cmp != 0 else recursive_compare(left[1:], right[1:])


with open('input.txt', 'r') as file:
    packets = list(map(lambda pair: list(map(eval, filter(lambda x: len(x) > 0, pair.split("\n")))),
                       file.read().split("\n\n")))

# PART ONE
print(sum((idx + 1) for idx, [left, right] in enumerate(packets) if recursive_compare(left, right) < 0))

# PART TWO
divider_left, divider_right = [[[2]], [[6]]]
c = Counter(map(lambda x: 'lower' if recursive_compare(x, divider_left) < 0
                                  else 'in middle' if recursive_compare(x, divider_right) < 0
                                  else 'higher',
                chain.from_iterable(packets)))
print((c['lower'] + 1) * (c['in middle'] + c['lower'] + 2))  # the two indices
