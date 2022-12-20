from collections import deque


def mixing(decr_key=1, n_times=1, filename='input.txt'):
    with open(filename, 'r') as file:
        data = deque(enumerate((int(line) * decr_key for line in file)))
    for _ in range(n_times):
        for idx in range(len(data)):
            while data[0][0] != idx:
                data.rotate(-1)

            ord_n, n_shift = data.popleft()
            data.rotate(-1 * n_shift)
            data.appendleft((ord_n, n_shift))

    return data


def find_coord(data):
    while data[0][1] != 0:
        data.rotate(-1)

    coord = list()
    for _ in range(3):
        for _ in range(1000):
            data.rotate(-1)
        coord.append(data[0][1])
    return sum(coord)


# PART ONE
print(find_coord(mixing()))

# PART TWO
print(find_coord(mixing(811589153, 10)))
