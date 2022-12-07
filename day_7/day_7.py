from collections import defaultdict
from itertools import accumulate
from operator import concat

total_space = 70000000
required_space = 30000000
max_size = 100000
curr_dir_path = list()
dir_tree = defaultdict(lambda: 0)


def keep_useful_info(entry):
    # keep only directory changes and file size
    return (True, entry[1]) if entry[0] == "$ cd" else (False, int(entry[0])) if entry[0][0].isdigit() else None


with open('input.txt', 'r') as file:
    commands = filter(bool, map(keep_useful_info, (line.strip('\n').rsplit(' ', 1) for line in file)))
    while True:
        try:
            change_dir, info = next(commands)
            if change_dir:
                curr_dir_path.pop() if info == ".." else curr_dir_path.append(info)
            else:
                for directory in accumulate(curr_dir_path, concat):  # the name of a directory is its path
                    dir_tree[directory] += info
        except StopIteration:
            break

# PART ONE
print(sum(filter(lambda x: x <= max_size, dir_tree.values())))

# PART TWO
to_del_space = required_space - (total_space - dir_tree["/"])  # required space - free space
print(to_del_space + min(filter(lambda x: x >= 0, map(lambda dir_size: dir_size - to_del_space, dir_tree.values()))))
