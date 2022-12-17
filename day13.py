
from collections import namedtuple
from functools import cmp_to_key
from more_itertools import flatten

Pair = namedtuple('Pair', ['left', 'right'])

def compare(left, right):

    if (type(left), type(right)) == (int, int):
        if left < right: return -1
        if left > right: return  1
        return  0

    if type(left) == int:
        left = [left]

    if type(right) == int:
        right = [right]

    for l, r in zip(left, right):
        result = compare(l , r)
        if result != 0: return result
    if len(left) < len(right): return -1
    if len(left) > len(right): return  1

    return 0  

def prepare(file_name):
    pairs = []
    with open(file_name, 'r') as infile:
        for pair in infile.read().split("\n\n"):
            first, second = pair.splitlines()
            pairs.append(Pair(eval(first), eval(second)))
    return pairs

def part_1(pairs):
    correct = list()
    for i, pair in enumerate(pairs):
        if compare(pair.left, pair.right) < 0:
            correct.append(i + 1)
    return sum(correct)

def part_2(pairs):
    key_1 = [[2]]
    key_2 = [[6]]
    packets = list(flatten(pairs))
    packets.append(key_1)
    packets.append(key_2)
    packets = sorted(packets, key=cmp_to_key(compare))
    index_1 = packets.index(key_1) + 1
    index_2 = packets.index(key_2) + 1
    return index_1 * index_2

if __name__ == '__main__':
    pairs = prepare('input/day13.txt')
    print("--------- Day 13 -----------")
    print(f"Part 1: { part_1(pairs) }")
    print(f"Part 2: { part_2(pairs) }")

#---------------------------------------------------------
import pytest

def test_pairs():
    pair1 = Pair([1,1,3,1,1], [1,1,5,1,1])
    assert compare(*pair1) < 0

    pair2 = Pair([[1],[2,3,4]], [[1],4])
    assert compare(*pair2) < 0

    pair3 = Pair([9], [[8,7,6]])
    assert not compare(*pair3) < 0

    pair4 = Pair([[4,4],4,4], [[4,4],4,4,4])
    assert compare(*pair4) < 0

    pair5 = Pair([7,7,7,7], [7,7,7])
    assert not compare(*pair5) < 0

    pair6 = Pair([], [3])
    assert compare(*pair6) < 0

    pair7 = Pair([[[]]], [[]])
    assert not compare(*pair7) < 0

    pair8 = Pair([1,[2,[3,[4,[5,6,7]]]],8,9], [1,[2,[3,[4,[5,6,0]]]],8,9])
    assert not compare(*pair8) < 0

def test_prepare():
    pairs = prepare('input/day13-example.txt')
    assert pairs[0].left == [1,1,3,1,1]
    assert pairs[6].left == [[[]]]

def test_part1():
    pairs = prepare('input/day13-example.txt')
    assert part_1(pairs) == 13

def test_part2():
    pairs = prepare('input/day13-example.txt')
    assert part_2(pairs) == 140
