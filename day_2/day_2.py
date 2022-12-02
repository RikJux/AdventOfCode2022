from enum import Enum
from itertools import tee, chain, repeat, groupby
from operator import itemgetter


class Shape(Enum):
    ROCK = 1
    PAPER = 2
    SCISSOR = 3


class Outcome(Enum):
    LOST = 0
    DRAW = 3
    WON = 6


def round_score(shape, outcome):
    return shape.value + outcome.value


def prepare_outcome_dict():
    """The dictionary is in the form:
    {opponent's move : {my move : round outcome}}

    """
    a, b = tee(Shape)
    b = chain(b, iter([next(b, None)]))  # put the first element in last position
    winning_combos = zip(a, b, repeat(Outcome.WON))

    a, b = tee(Shape)
    drawing_combos = zip(a, b, repeat(Outcome.DRAW))

    a, b = tee(Shape)
    a = chain(a, iter([next(a, None)]))  # put the first element in last position
    losing_combos = zip(a, b, repeat(Outcome.LOST))

    all_combos = sorted(chain(winning_combos, drawing_combos, losing_combos), key=lambda x: x[0].value)
    return dict(map(lambda x: (x[0], dict(map(lambda y: (y[1], y[2]), x[1]))), groupby(all_combos, lambda x: x[0])))


outcome_dict = prepare_outcome_dict()
# just invert the inner dicts to get the mapping {opponent's move: {round outcome: my move}}
required_shape_dict = {k1: {v: k2 for k2, v in outcome_dict[k1].items()} for k1 in outcome_dict.keys()}


def compute_outcome(opponent_shape, my_shape):
    return outcome_dict[opponent_shape][my_shape]


def required_shape(opponent_shape, required_outcome):
    return required_shape_dict[opponent_shape][required_outcome]


def encryption_dict(encrypted_list, e) -> dict:
    return dict(zip(encrypted_list, e))


def decrypt(encryption, encrypted_arg):
    return encryption[encrypted_arg]


def compute_total_score(opp_dict, my_dict, dict_entry,
                        my_shape_fun, outcome_fun, file_name='input.txt'):
    with open(file_name, 'r') as file:
        rounds = (line.strip('\n').split(" ") for line in file)
        decrypted_rounds = map(lambda x: {"opponent_shape": decrypt(opp_dict, x[0]),
                                          dict_entry: decrypt(my_dict, x[1])}, rounds)

        total_score = sum(map(lambda x: round_score(my_shape_fun(x), outcome_fun(x)), decrypted_rounds))
        return total_score


opponent_play = encryption_dict(['A', 'B', 'C'], Shape)

# PART ONE: the second column represents the shape to play
entry = "my_shape"
my_play = encryption_dict(['X', 'Y', 'Z'], Shape)
part_one_input = (opponent_play, my_play, entry,
                  itemgetter(entry), lambda x: compute_outcome(**x))

print(compute_total_score(*part_one_input))

# PART TWO: the second column represents the desired outcome to reach
entry = "required_outcome"
my_outcome = encryption_dict(['X', 'Y', 'Z'], Outcome)
part_two_input = (opponent_play, my_outcome, entry,
                  lambda x: required_shape(**x), itemgetter(entry))

print(compute_total_score(*part_two_input))
