from itertools import takewhile
from heapq import nlargest, heappush

top = 3

with open('input.txt', 'r') as file:
    calories = (line.strip('\n') for line in file)
    calories_heap = list()
    while True:
        elf_calories = sum(map(int, takewhile(lambda x: x != '', calories)))
        if elf_calories == 0:  # there are no more elves
            break
        heappush(calories_heap, elf_calories)

    top_calories = nlargest(top, calories_heap)
    print(top_calories)
    print(sum(top_calories))
