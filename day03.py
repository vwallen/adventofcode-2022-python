from string import ascii_lowercase, ascii_uppercase

CODES = "_" + ascii_lowercase + ascii_uppercase

def prepare(file_path):
    with open(file_path, 'r') as infile:
        output = [line.rstrip() for line in infile.readlines()]
    return output

def chunk(sequence, size):
    return [sequence[i : i+size] for i in range(0, len(sequence), size)]

def part_1(input):
    rucksacks = [(line[:len(line)//2], line[len(line)//2:]) for line in input]
    intersects = [(set(a) & set(b)).pop() for a, b in rucksacks]
    values = [CODES.index(c) for c in intersects]
    return sum(values)

def part_2(input):
    badges = []
    for a, b, c in chunk(input, 3):
        badge = (set(a) & set(b) & set(c)).pop()
        badges.append(CODES.index(badge))
    return sum(badges)

if __name__ == '__main__':
    input = prepare('input/day03.txt')
    print("--------- Day 3 -----------")
    print("Part 1: %s" % part_1(input))
    print("Part 2: %s" % part_2(input))

#---------------------------------------------------------------
import pytest

@pytest.fixture
def example():
    return prepare('input/day03-example.txt')

def test_prepare_input(example):
    assert example[0] == 'vJrwpWtwJgWrhcsFMMfFFhFp'
    assert example[4] == 'ttgJtRGJQctTZtZT'

def test_part_1(example):
    assert part_1(example) == 157

def test_part_2(example):
    assert part_2(example) == 70
