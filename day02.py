from enum import IntEnum 

class Outcome(IntEnum):
    Win = 6
    Lose = 0
    Draw = 3

class Play(IntEnum):
    Rock = 1
    Paper = 2
    Scissors = 3

PLAY_CODES = {
    'A': Play.Rock,
    'X': Play.Rock,
    'B': Play.Paper,
    'Y': Play.Paper,
    'C': Play.Scissors,
    'Z': Play.Scissors,
}

OUTCOME_CODES = {
    'X': Outcome.Lose,
    'Y': Outcome.Draw,
    'Z': Outcome.Win,
}

PRECEDENCE = (Play.Rock, Play.Paper, Play.Scissors) * 2

def calculate_score(p1, p2):
    if p1 == p2:
        return Outcome.Draw + p1
    else:
        return {
            (Play.Rock, Play.Scissors): Outcome.Win + p1,
            (Play.Paper, Play.Rock): Outcome.Win + p1,
            (Play.Scissors, Play.Paper): Outcome.Win + p1,
        }.get((p1, p2), p1 + Outcome.Lose)

def calculate_score2(p1, result):
    return result + {
        Outcome.Win:  PRECEDENCE[p1],
        Outcome.Lose: PRECEDENCE[p1 + 1],
        Outcome.Draw: p1,
    }.get(result, 0)

def prepare(file_path):
    with open(file_path, 'r') as infile:
        output = [tuple(line.strip().split(" ")) for line in infile.readlines()]
    return output

def part_1(input):
    results = []
    for result in input:
        results.append(calculate_score(
            PLAY_CODES.get(result[1]),
            PLAY_CODES.get(result[0]),
        ))
    return sum(results)

def part_2(input):
    results = []
    for result in input:
        results.append(calculate_score2(
            PLAY_CODES.get(result[0]),
            OUTCOME_CODES.get(result[1]),
        ))
    return sum(results)

if __name__ == '__main__':
    input = prepare('input/day02.txt')
    print("--------- Day 2 -----------")
    print("Part 1: %s" % part_1(input))
    print("Part 2: %s" % part_2(input))


#---------------------------------------------------------------
import pytest

@pytest.fixture
def example():
    return prepare('input/day02-example.txt')

def test_prepare_input(example):
    assert example[0] == ('A', 'Y')
    assert example[-1] == ('C', 'Z')

def test_outcomes_1():
    assert calculate_score(Play.Rock, Play.Scissors) == Play.Rock + Outcome.Win
    assert calculate_score(Play.Scissors, Play.Rock) == Play.Scissors + Outcome.Lose
    assert calculate_score(Play.Paper, Play.Rock) == Play.Paper + Outcome.Win

def test_outcomes_2():
    assert calculate_score2(Play.Scissors, Outcome.Win) == Play.Rock + Outcome.Win
    assert calculate_score2(Play.Rock, Outcome.Lose) == Play.Scissors + Outcome.Lose

def test_part_1(example):
    assert part_1(example) == 15

def test_part_2(example):
    assert part_2(example) == 12