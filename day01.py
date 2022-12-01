def prepare(file_path):
    with open(file_path, 'r') as infile:
        elves = [tuple(map(int, elf.splitlines())) for elf in infile.read().split("\n\n")]
    return elves

def part_1(elves):
    return max(map(sum, elves))

def part_2(elves):
    return sum(sorted(map(sum, elves))[-3:])    

if __name__ == '__main__':
    elves = prepare('input/day01.txt')
    print("Part 1: %s" % part_1(elves))
    print("Part 2: %s" % part_2(elves))

#---------------------------------------------------------------
import pytest

@pytest.fixture
def example_elves():
    return prepare('input/day01-example.txt')

def test_prepare_input(example_elves):
    assert example_elves[0] == (1000, 2000, 3000)
    assert example_elves[-1] == (10000,)

def test_part_1(example_elves):
    assert part_1(example_elves) == 24000

def test_part_2(example_elves):
    assert part_2(example_elves) == 45000
