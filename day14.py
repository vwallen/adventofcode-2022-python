import colored
import parse
from collections import namedtuple, deque, defaultdict
from more_itertools import pairwise, flatten

P = namedtuple('P', ['x', 'y'])
S = namedtuple('S', ['p1', 'p2'])

def prepare(file_path):
    segments = list()
    with open(file_path, 'r') as infile:
        for line in infile.read().splitlines():
            matches = parse.findall("{xcoord:d},{ycoord:d}", line)
            path = list()
            for match in matches:
                path.append(P(match['xcoord'], match['ycoord']))
            segments.extend(map(lambda p: S(p[0], p[1]), pairwise(path)))
    return segments

def get_bounds(segments):
    all_points = set(flatten(segments))
    min_x = min(map(lambda p: p.x, all_points))
    max_x = max(map(lambda p: p.x, all_points))
    max_y = max(map(lambda p: p.y, all_points))
    return S(P(min_x, 0), P(max_x, max_y))

def get_bounds_checker(segments):
    bounds = get_bounds(segments)
    def in_bounds(p):
        return not (bounds.p1.x > p.x or p.x > bounds.p2.x or 
                    bounds.p1.y > p.y or p.y > bounds.p2.y)
    return in_bounds

def get_floor_checker(segments):
    bounds = get_bounds(segments)
    def in_bounds(p):
        return not (bounds.p1.y > p.y or p.y > bounds.p2.y + 2)
    return in_bounds

def draw_cave(bounds, locations, walls):
    offset = bounds.p1.x

    grid = list()
    for y in range(bounds.p2.y - bounds.p1.y + 5):
        grid.append(list())
        for x in range(bounds.p2.x - bounds.p1.x + 10):
            grid[y].append(None)

    for loc, moves in locations.items():
        p = P(loc.x - offset + 1, loc.y)
        try:
            grid[p.y][p.x] = moves
        except IndexError:
            pass # ignore out of bounds from infinite floor

    for wall in walls:
        w = P(wall.x - offset + 1, wall.y)
        try:
            grid[w.y][w.x] = -1
        except IndexError:
            pass # ignore out of bounds from infinite floor

    out = ""
    for row in grid:
        for col in row:
            if col is not None:
                if col == -1:
                    out += colored.fg(250) + "█"
                elif col == 0:
                    out += colored.fg(222) + "▒"
            else:
                out += " "
        out += "\n"
    return out

def get_walls(segments):
    walls = set()
    for seg in segments:
        if seg.p1.y == seg.p2.y: # horizontal
            x1 = min(seg.p1.x, seg.p2.x)
            x2 = max(seg.p1.x, seg.p2.x)
            y  = seg.p1.y
            [walls.add(P(x, y)) for x in range(x1, x2 + 1)]
        else:                    # vertical
            y1 = min(seg.p1.y, seg.p2.y)
            y2 = max(seg.p1.y, seg.p2.y)
            x  = seg.p1.x
            [walls.add(P(x, y)) for y in range(y1, y2 + 1)]
    return walls

def scan(walls, start, in_bounds):

    locations = defaultdict(lambda: 3)
    stationary = set()
    search_path = deque()
    cursor = start

    while in_bounds(cursor):

        next_pos = None
        moves = locations[cursor]

        # check down
        if moves == 3: # open/unchecked down
            next_pos = P(cursor.x, cursor.y + 1)
            if next_pos in walls or next_pos in stationary:
                moves += -1

        # check down left
        if moves == 2: # open/unchecked down left
            next_pos = P(cursor.x - 1, cursor.y + 1)
            if next_pos in walls or next_pos in stationary:
                moves += -1

        # check down right
        if moves == 1: # open/unchecked down right
            next_pos = P(cursor.x + 1, cursor.y + 1)
            if next_pos in walls or next_pos in stationary:
                moves += -1

        locations[cursor] = moves

        if moves == 0: # blocked
            stationary.add(cursor)
            if search_path:
                # back up to check previous again
                cursor = search_path.pop()
            else:
                cursor = None
                break
        else:
            search_path.append(cursor)
            cursor = next_pos

    return locations, stationary
#-------------------------------------------------------------

def part_1(segments):
    walls = get_walls(segments)
    start = P(500, 0)
    in_bounds = get_bounds_checker(segments)
    locations, stationary = scan(walls, start, in_bounds)
    print("\n" + draw_cave(get_bounds(segments), locations, walls))
    return len(stationary)

def part_2(segments):
    walls = get_walls(segments)
    bounds = get_bounds(segments)
    for x in range(500): # add infinite floor
        walls.add(P(500 - x, bounds.p2.y + 2))
        walls.add(P(500 + x, bounds.p2.y + 2))
    start = P(500, 0)
    in_bounds = get_floor_checker(segments)
    locations, stationary = scan(walls, start, in_bounds)
    print("\n" + draw_cave(get_bounds(segments), locations, walls))
    return len(stationary)

if __name__ == '__main__':
    segments = prepare('input/day14.txt')
    print("--------- Day 8 -----------")
    print("Part 1: %s" % part_1(segments))
    print("---------------------------")
    print("Part 2: %s" % part_2(segments))
    
#-------------------------------------------------------------
import pytest

def test_prepare():
    segments = prepare('input/day14-example.txt')

def test_bounds_checking():
    segments = prepare('input/day14-example.txt')
    in_bounds = get_bounds_checker(segments)
    assert in_bounds(P(494, 0))
    assert in_bounds(P(503, 9))
    assert not in_bounds(P(493, -1))
    assert not in_bounds(P(504, 10))

def test_part_1():
    segments = prepare('input/day14-example.txt')
    assert part_1(segments) == 24

def test_part_2():
    segments = prepare('input/day14-example.txt')
    assert part_2(segments) == 93
