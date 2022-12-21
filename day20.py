from math import fmod, copysign
from collections import namedtuple

V = namedtuple('V', ['value', 'index'])

def prepare(file_name):
    values = list()
    with open(file_name, 'r') as infile:
        lines = infile.readlines()
        for line in lines:
            values.append(int(line.strip()))
    return values

def mix(sequence, values):
    for v in sequence:

        if v.value == 0: continue
        index_from = values.index(v)
        values.pop(index_from)

        wrap = len(values)
        insert_to = (index_from + v.value) % wrap
        if insert_to == 0: insert_to = wrap

        values.insert(insert_to, v)

def score(values):
    mixed = [v.value for i, v in enumerate(values)]
    start = mixed.index(0)
    wrap = len(mixed)
    n1000 = mixed[(start + 1000) % wrap]
    n2000 = mixed[(start + 2000) % wrap]
    n3000 = mixed[(start + 3000) % wrap]
    return sum([n1000, n2000, n3000])    

def part_1(raw_values):
    values = list()
    for i, v in enumerate(raw_values):
        values.append(V(v, i))

    mix(values[:], values)
    return score(values)

def part_2(raw_values):
    KEY = 811589153
    values = list()
    for i, v in enumerate(raw_values):
        values.append(V(v * KEY, i))
    sequence = values[:]
    for _ in range(10):
        mix(sequence, values)
    return score(values)

if __name__ == '__main__':
    print("--------- Day 20 -----------")
    print(f"Part 1: { part_1(prepare('input/day20.txt')) }")

    print("---------------------------")
    print(f"Part 2: { part_2(prepare('input/day20.txt')) }")