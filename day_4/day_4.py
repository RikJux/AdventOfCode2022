def do_contain(range_1, range_2):
    range_1, range_2 = sorted([range_1, range_2])
    if range_1[1] >= range_2[1]:
        return 1
    if range_1[0] == range_2[0] and range_1[1] <= range_2[1]:
        return 1
    return 0


def do_overlap(range_1, range_2):
    range_1, range_2 = sorted([range_1, range_2])
    if range_1[1] >= range_2[0]:
        return 1
    return 0


def compute_n_overlap(filename, function):
    with open(filename, 'r') as file:
        return sum(map(lambda pair_sectors: function(*(list(map(int, sectors.split("-"))) for sectors in pair_sectors)),
                       (line.strip("\n").split(",") for line in file)))


# PART ONE
print(compute_n_overlap('input.txt', do_contain))

# PART TWO
print(compute_n_overlap('input.txt', do_overlap))
