import cairo
import math
import parse
from collections import namedtuple
from more_itertools import pairwise, flatten
from pprint import PrettyPrinter

pp = PrettyPrinter()

P = namedtuple('P', ['x', 'y'])
S = namedtuple('S', ['p1', 'p2'])

def prepare(file_path):
    segments = list()
    with open(file_path, 'r') as infile:
        input = infile.read().splitlines()

    for line in input:
        matches = parse.findall("{xcoord:d},{ycoord:d}", line)
        path = list()
        for match in matches:
            path.append(P(match['xcoord'], match['ycoord']))
        segments.extend(map(lambda p: S(p[0], p[1]), pairwise(path)))
    return segments

def get_bounds(segments):
    all_points = set(flatten(segments))
    min_x, max_x = min(map(lambda p: p.x, all_points)), max(map(lambda p: p.x, all_points))
    min_y, max_y = min(map(lambda p: p.y, all_points)), max(map(lambda p: p.y, all_points))
    return S(P(min_x, 0), P(max_x + 5, max_y + 5))

def draw_cave(segments):
    bounds = get_bounds(segments)
    offset = bounds.p1.x

    grid = list()
    for y in range(bounds.p2.y - bounds.p1.y):
        grid.append(list())
        for x in range(bounds.p2.x - bounds.p1.x):
            grid[y].append(0)

    print(f" GRID: {len(grid[0])}x{len(grid)}")

    for seg in segments:
        is_horiz = seg.p1.y == seg.p2.y
        if is_horiz:
            x1 = min(seg.p1.x, seg.p2.x)
            x2 = max(seg.p1.x, seg.p2.x)
            for x in range(x1 - offset, x2 - offset + 1):
                grid[seg.p1.y][x] = 1
        else:
            y1 = min(seg.p1.y, seg.p2.y)
            y2 = max(seg.p1.y, seg.p2.y)
            for y in range(y1, y2 + 1):
                grid[y][seg.p1.x - offset] = 1

        for y, row in enumerate(grid):
            x = 500 - offset
            if grid[y][x] == 0:
                grid[y][x] = 2

    out = ""
    for row in grid:
        for col in row:
            if col == 0:
                out += " "
            if col == 1:
                out += "█"
            if col == 2:
                out += "░"
        out += "\n"
    print(out)

#-------------------------------------------------------------
import pytest

def test_prepare():
    segments = prepare('input/day14.txt')
    print("\n\n")
    draw_cave(segments)



