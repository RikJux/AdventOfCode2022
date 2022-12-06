from collections import deque

packet_marker_size = 4
msg_marker_size = 14


def start_of_detected(deque_size, filename='input.txt'):
    seen = deque(maxlen=deque_size)
    with open(filename, 'r') as file:
        for idx, signal in filter(lambda x: x != "\n", enumerate(file.read())):
            seen.append(signal)
            if len(set(seen)) == deque_size:  # no duplicates
                return idx + 1


print(start_of_detected(packet_marker_size))  # PART ONE
print(start_of_detected(msg_marker_size))  # PART TWO
