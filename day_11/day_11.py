from operator import add, mul, pow
from itertools import chain, repeat
from functools import partial, reduce
from collections import deque
from heapq import nlargest


class Monkey:
    def __init__(self, string, divide_worry):
        monkey_id, items, operation, divisible_test, if_case, else_case = filter(lambda x: x != '', string.split("\n"))
        self.monkey_id = int(monkey_id.split(" ")[1][:-1])
        self.items = deque(map(int, items.split(": ")[1].split(", ")))
        op, el = operation.split("old ")[1].split(" ")
        if op == "+":
            op = partial(add, int(el))
        elif op == "*":
            if el == "old":
                op = partial(lambda x, y: pow(x, y), y=2)
            else:
                op = partial(mul, int(el))
        else:
            raise NotImplementedError
        self.worry_change = op
        self.divisible_test = int(divisible_test.split(" ")[-1])
        self.if_case = int(if_case.split(" ")[-1])
        self.else_case = int(else_case.split(" ")[-1])
        self.divide_worry = divide_worry

        self.mod_worry = None
        self.monkey_dict = None
        self.n_inspections = 0

    def turn(self):
        while len(self.items) > 0:
            item = self.items.popleft()
            item = (self.worry_change(item) // self.divide_worry)
            item = (item % self.mod_worry) if self.mod_worry else item
            self.n_inspections += 1
            if item % self.divisible_test == 0:
                target_monkey = self.if_case
            else:
                target_monkey = self.else_case
            self.throw_item(item, self.monkey_dict[target_monkey])

    def get_item(self, item):
        self.items.append(item)

    def throw_item(self, item, monkey):
        monkey.get_item(item)


def monkey_business(filename, n_turns, divide_worry=1, n_largest=2):
    with open(filename, 'r') as file:
        monkeys = list(map(lambda x: Monkey(x, divide_worry), file.read().split("\n\n")))

    mod_worry = reduce(mul, (monkey.divisible_test for monkey in monkeys), 1)
    monkey_dict = dict(((monkey.monkey_id, monkey) for monkey in monkeys))

    for monkey in monkeys:
        monkey.mod_worry = mod_worry  # not strictly necessary in part one
        monkey.monkey_dict = monkey_dict

    for monkey in chain.from_iterable(repeat(monkeys, n_turns)):
        monkey.turn()

    return mul(*nlargest(n_largest, [monkey.n_inspections for monkey in monkeys]))


# PART ONE
print(monkey_business('input.txt', 20, 3))

# PART TWO
print(monkey_business('input.txt', 10000))
