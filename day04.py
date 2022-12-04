def parse_range(r):
    m, n = r.split("-")
    return set(range(int(m), int(n)+1))

def prepare(file_path):
    output = []
    with open(file_path, 'r') as infile:
        for line in infile.readlines():
            a, b = line.split(",")
            output.append((parse_range(a), parse_range(b)))
    return output


def part_1(input):
    results = 0
    for pair in input:
        if len(pair[0] & pair[1]) in (len(a) for a in pair):
            results += 1
    return results

def part_2(input):
    results = 0
    for pair in input:
        if len(pair[0] & pair[1]) > 0:
            results += 1
    return results

if __name__ == '__main__':
    input = prepare('input/day04.txt')
    print("--------- Day 3 -----------")
    print("Part 1: %s" % part_1(input))
    print("Part 2: %s" % part_2(input))

#---------------------------------------------------------------
import pytest

@pytest.fixture
def example():
    return prepare('input/day04-example.txt')

def test_prepare_input(example):
    assert example[0] == ({2, 3, 4}, {6, 7, 8})

def test_part_1(example):
    assert part_1(example) == 2

def test_part_2(example):
    assert part_2(example) == 4
