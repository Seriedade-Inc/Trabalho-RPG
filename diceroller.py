import random

#SUPPORTED_DICE = {d4, d6, d8, d10, d12, d20, d100}


def roll_dice(num_dice, sides):
    return sum(random.randint(1, sides) for _ in range(num_dice))


def roll_die(sides):
    return roll_dice(1, sides)


def roll_d4():
    return roll_die(4)


def roll_d6():
    return roll_die(6)


def roll_d8():
    return roll_die(8)


def roll_d10():
    return roll_die(10)


def roll_d12():
    return roll_die(12)


def roll_d20():
    return roll_die(20)


def roll_d100():
    return roll_die(100)
