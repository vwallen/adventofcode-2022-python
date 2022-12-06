def prepare(file_path):
    with open(file_path, 'r') as infile:
        stream = infile.read().rstrip()
    return stream

def find_marker(stream, span):
    for i in range(len(stream)):
        if len(set(stream[i:i+span])) == span:
            return i + span
    return -1

def part_1(stream):
    return find_marker(stream, 4)

def part_2(stream):
    return find_marker(stream, 14)

if __name__ == '__main__':
    stream = prepare('input/day06.txt')
    print("Part 1: %s" % part_1(stream))
    print("Part 2: %s" % part_2(stream))

#---------------------------------------------------------------
import pytest


def test_part_1():
    assert part_1("mjqjpqmgbljsphdztnvjfqwrcgsmlb") == 7
    assert part_1("bvwbjplbgvbhsrlpgdmjqwftvncz") == 5
    assert part_1("nppdvjthqldpwncqszvftbrmjlhg") == 6
    assert part_1("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg") == 10
    assert part_1("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw") == 11

def test_part_2():
    assert part_2("mjqjpqmgbljsphdztnvjfqwrcgsmlb") == 19
    assert part_2("bvwbjplbgvbhsrlpgdmjqwftvncz") == 23
    assert part_2("nppdvjthqldpwncqszvftbrmjlhg") == 23
    assert part_2("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg") == 29
    assert part_2("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw") == 26
