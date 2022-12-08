import pprint
from itertools import *

pp = pprint.PrettyPrinter()

class Tree:
    def __init__(self, height):
        self.height = height
        self.visible = False
        self.score = 0

def prepare(file_path):
    trees = []

    with open(file_path, 'r') as infile:
        lines = infile.read().splitlines()

    for line in lines:
        row = []
        w = len(line)
        for ch in line:
            row.append(Tree(int(ch)))
        trees.append(row)

    return trees

def part_1(trees):

    rows = len(trees)
    cols = len(trees[0])

    for r in range(rows):
        tallest_west = -1
        tallest_east = -1
        for c in range(cols):
            tree = trees[r][c]
            tree.visible |= tree.height > tallest_west
            tallest_west = max(tree.height, tallest_west)

            tree = trees[r][-(c+1)]
            tree.visible |= tree.height > tallest_east
            tallest_east = max(tree.height, tallest_east)

    for c in range(cols):
        tallest_north = -1
        tallest_south = -1
        for r in range(rows):
            tree = trees[r][c]
            tree.visible |= tree.height > tallest_north
            tallest_north = max(tree.height, tallest_north)

            tree = trees[-(r+1)][c]
            tree.visible |= tree.height > tallest_south
            tallest_south = max(tree.height, tallest_south)

    return len(list(filter(lambda tree: tree.visible, list(chain(*trees)))))

def score_view(height, trees):
    score = 0
    for i, tree in enumerate(trees[:]):
        score = i + 1
        if tree.height >= height:
            break
    return score

def part_2(trees):
    
    rows = len(trees)
    cols = len(trees[0])

    scenic_score = 0

    for r in range(rows):
        for c in range(cols):
            tree = trees[r][c]
            w = score_view(tree.height, trees[r][:c][::-1])
            e = score_view(tree.height, trees[r][c+1:])
            n = score_view(tree.height, [row[c] for row in trees][:r][::-1])
            s = score_view(tree.height, [row[c] for row in trees][r+1:])
            tree.score = w * e * n * s
            scenic_score = max(tree.score, scenic_score)

    return scenic_score

if __name__ == '__main__':
    trees = prepare('input/day08.txt')

    print("--------- Day 8 -----------")
    print("Part 1: %s" % part_1(trees))
    print("Part 2: %s" % part_2(trees))

#---------------------------------------------------------------
import pytest

@pytest.fixture
def trees():
    return prepare('input/day08-example.txt')

def test_part_1(trees):
    assert part_1(trees) == 21

def test_part_2(trees):
    assert part_2(trees) == 8
