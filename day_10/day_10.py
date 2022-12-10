from itertools import accumulate
from more_itertools import map_if, flatten, chunked

required_values = range(20, 221, 40)
screen_wide = 40

with open('input.txt', 'r') as file:
    program = map_if(((line.strip("\n").split(" ") for line in file)),
                     lambda x: x[0] == 'addx', lambda x: ['noop', int(x[1])])
    cpu_vals = list(accumulate(map_if(flatten(program), lambda x: x == 'noop', lambda x: 0), initial=1))

    # PART ONE
    print(sum(cpu_vals[idx-1]*idx for idx in required_values))

    # PART TWO
    pixels = ('#' if abs((drawing % screen_wide)-x_val) < 2 else '.' for drawing, x_val in enumerate(cpu_vals))
    print('\n'.join(list(map(lambda x: ''.join(x), chunked(pixels, screen_wide)))))
