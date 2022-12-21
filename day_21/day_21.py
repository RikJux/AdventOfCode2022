from re import search
from sympy import symbols, solve

with open('input.txt', 'r') as file:
    monkeys = dict(line.strip("\n").split(": ") for line in file)


def generate_equation(eq):
    while True:
        variable = search(r'[a-z]{4}', eq)
        if not variable:
            break
        else:
            eq = eq[:variable.start()] + \
                     "(" + monkeys[variable.group()] + ")" + \
                 eq[variable.end():]

    return eq


# PART ONE
print(int(eval(generate_equation(monkeys['root']))))

# PART TWO
x = symbols('x')
monkeys['humn'] = "x"
monkeys['root'] = " - ".join(monkeys['root'].split(" ")[0:3:2])
print(int(solve(eval(generate_equation(monkeys['root'])), x)[0]))
