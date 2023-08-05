from FedxD  import Lists
import random


def date(year):
    month = random.randint(1, 12)
    if month == 2:
        day = random.randint(1, 28)
    else:
        day = random.randint(1, 30)
        date = f"{day}/{month}/{year}"
        return date


def color():
    return random.choice(Lists.color_list())


def name():
    return random.choice(Lists.name_list())


def age():
    return random.randint(1, 80)


def fact():
    return random.choice(Lists.fact_list())


def true_false():
    return random.choice([True, False])
