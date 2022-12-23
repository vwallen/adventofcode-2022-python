from collections import deque, namedtuple, OrderedDict
from more_itertools import chunked
from math import sqrt

P = namedtuple('P', ['x', 'y'])

EAST  = 0
SOUTH = 1
WEST  = 2
NORTH = 3

facings = OrderedDict()
facings[EAST]  = P( 1, 0)
facings[SOUTH] = P( 0, 1)
facings[WEST]  = P(-1, 0)
facings[NORTH] = P( 0,-1)

RIGHT =  1
LEFT  = -1

def sum_vecs(a, b):
    return P(a.x + b.x, a.y + b.y)

class Walker:
    def __init__(self, pos, facing):
        self.facing = facing
        self.pos = pos
        

def prepare(file_name):
    with open(file_name, 'r') as infile:
        map_str, command_str = infile.read().split("\n\n")

    zone_map = dict()
    wall_map = set()
    for y, line in enumerate(map_str.splitlines()):
        for x, ch in enumerate(line):
            if ch == '.':
                zone_map[P(x, y)] = 0
            elif ch == '#':
                zone_map[P(x, y)] = 1
                wall_map.add(P(x, y))

    commands = deque()
    d = ""
    for ch in command_str:
        if ch.isdigit():
            d += ch
        else:
            commands.append(int(d))
            commands.append(ch)
            d = ""
    else:
        commands.append(int(d))

    return zone_map, wall_map, commands

def render_map(path_map, loc=None, path=[]):
    w = max({x for x,y in path_map.keys()}) + 1
    h = max({y for x,y in path_map.keys()}) + 1
    map_str = " " * w * h
    for k, v in path_map.items():
        i = k.x + k.y * w
        if v == 0:
            map_str = map_str[:i] + '.' + map_str[i+1:]
        elif v == 1:
            map_str = map_str[:i] + '#' + map_str[i+1:]

    if loc is not None:
        i = loc.x + loc.y * w
        map_str = map_str[:i] + '@' + map_str[i+1:]

    for pos in path:
        x, y, f = pos
        ch = '>'
        if f == 1: ch = 'v'
        if f == 2: ch = '<'
        if f == 3: ch = '^'
        i = x + y * w
        map_str = map_str[:i] + ch + map_str[i+1:]

    map_str = '\n'.join(map(lambda row: ''.join(row), chunked(map_str, w)))
    return map_str

def part_1(zone_map, wall_map, commands):

    start_pos = P(min(x for x, y in zone_map.keys() if y == 0), 0)
    walker = Walker(start_pos, EAST)
    path = list()
    for cmd in commands:
        if type(cmd) == int:
            for _ in range(cmd):
                next_pos = sum_vecs(walker.pos, facings[walker.facing])
                if next_pos not in zone_map:
                    if   walker.facing == 0:
                        next_pos = P(min(x for x, y in zone_map.keys() if y == next_pos.y), next_pos.y)
                    elif walker.facing == 2:
                        next_pos = P(max(x for x, y in zone_map.keys() if y == next_pos.y), next_pos.y)
                    elif walker.facing == 1:
                        next_pos = P(next_pos.x, min(y for x, y in zone_map.keys() if x == next_pos.x))
                    elif walker.facing == 3:
                        next_pos = P(next_pos.x, max(y for x, y in zone_map.keys() if x == next_pos.x))
                if next_pos in wall_map: continue
                path.append((walker.pos.x, walker.pos.y, walker.facing))
                walker.pos = next_pos
        if cmd == 'L':
            walker.facing = (walker.facing + LEFT) % 4
        if cmd == 'R':
            walker.facing = (walker.facing + RIGHT) % 4

    adjusted_pos = sum_vecs(walker.pos, P(1, 1))
    return 1000 * adjusted_pos.y + 4 * adjusted_pos.x + walker.facing

# --------------------------------------------------------------------------------------
# PUZZLE INPUT DATA
#                   6>    6^
#                + - - + - - +
#                |     |     |
#              4>|  1  |  2  |5<
#                |     |     |
#                + - - + - - +
#                |     |  3<
#              4v|  3 >|2^
#             3> |     | 
#          + - - + - - +
#          |     |     |
#        1>|  4  |  5  |2<
#          |     |     |
#          + - - + - - +
#          |     |  6<
#        1v|  6  |5^
#          |     |
#          + - - +
#             2v
def zone_to_zone(from_facing, to_facing):
    to_zone = {
        1: {EAST: (2, EAST),  SOUTH: (3, SOUTH), WEST: (4, EAST),  NORTH: (6, EAST)},
        2: {EAST: (5, WEST),  SOUTH: (3, WEST),  WEST: (1, WEST),  NORTH: (6, NORTH)},
        3: {EAST: (2, NORTH), SOUTH: (5, SOUTH), WEST: (4, SOUTH), NORTH: (1, NORTH)},
        4: {EAST: (5, EAST),  SOUTH: (6, SOUTH), WEST: (1, EAST),  NORTH: (3, EAST)},
        5: {EAST: (2, WEST),  SOUTH: (6, WEST),  WEST: (4, WEST),  NORTH: (3, NORTH)},
        6: {EAST: (5, NORTH), SOUTH: (2, SOUTH), WEST: (1, SOUTH), NORTH: (4, NORTH)},
    }
    return to_zone[from_facing][to_facing]

def map_to_zone(zone_dim, z, p):
    _map_to_zone = {
        1: lambda p: P(p.x - (1 * zone_dim), p.y - (0 * zone_dim)),
        2: lambda p: P(p.x - (2 * zone_dim), p.y - (0 * zone_dim)),
        3: lambda p: P(p.x - (1 * zone_dim), p.y - (1 * zone_dim)),
        4: lambda p: P(p.x - (0 * zone_dim), p.y - (2 * zone_dim)),
        5: lambda p: P(p.x - (1 * zone_dim), p.y - (2 * zone_dim)),
        6: lambda p: P(p.x - (0 * zone_dim), p.y - (3 * zone_dim)),
    }
    return _map_to_zone[z](p)

def zone_to_map(zone_dim, z, p):
    _zone_to_map = {
        1: lambda p: P(p.x + (1 * zone_dim), p.y + (0 * zone_dim)),
        2: lambda p: P(p.x + (2 * zone_dim), p.y + (0 * zone_dim)),
        3: lambda p: P(p.x + (1 * zone_dim), p.y + (1 * zone_dim)),
        4: lambda p: P(p.x + (0 * zone_dim), p.y + (2 * zone_dim)),
        5: lambda p: P(p.x + (1 * zone_dim), p.y + (2 * zone_dim)),
        6: lambda p: P(p.x + (0 * zone_dim), p.y + (3 * zone_dim)),
    }
    return _zone_to_map[z](p)

def which_zone(zone_dim, p):
    col = p.x // zone_dim
    row = p.y // zone_dim
    lookup = [
        [0,1,2],
        [0,3,0],
        [4,5,0],
        [6,0,0],
    ]
    zone = lookup[row][col]
    return zone
# --------------------------------------------------------------------------------------


def part_2(zone_map, wall_map, commands):

    zone_dim = int(sqrt(len(zone_map)/6))

    start_pos = P(min(x for x, y in zone_map.keys() if y == 0), 0)
    walker = Walker(start_pos, EAST)
    path = list()
    for cmd in commands:
        if type(cmd) == int:
            for _ in range(cmd):
                next_pos    = sum_vecs(walker.pos, facings[walker.facing])
                next_facing = walker.facing
                if next_pos not in zone_map:
                    walker_zone = which_zone(zone_dim, walker.pos)
                    max_index = zone_dim - 1
                    next_zone, next_facing = zone_to_zone(walker_zone, walker.facing)
                    zone_pos = map_to_zone(zone_dim, walker_zone, walker.pos)
                    next_zone_pos = zone_pos

                    if walker.facing == EAST:
                        if next_facing == SOUTH: next_zone_pos = P(max_index - zone_pos.y, max_index - zone_pos.x)
                        if next_facing == NORTH: next_zone_pos = P(zone_pos.y, zone_pos.x)
                        if next_facing == EAST:  next_zone_pos = P(max_index - zone_pos.x, zone_pos.y)
                        if next_facing == WEST:  next_zone_pos = P(zone_pos.x, max_index - zone_pos.y)

                    if walker.facing == SOUTH:
                        if next_facing == EAST:  next_zone_pos = P(max_index - zone_pos.y, max_index - zone_pos.x)
                        if next_facing == WEST:  next_zone_pos = P(zone_pos.y, zone_pos.x)
                        if next_facing == NORTH: next_zone_pos = P(max_index - zone_pos.x, zone_pos.y)
                        if next_facing == SOUTH: next_zone_pos = P(zone_pos.x, max_index - zone_pos.y)

                    if walker.facing == WEST:
                        if next_facing == NORTH: next_zone_pos = P(max_index - zone_pos.y, max_index - zone_pos.x)
                        if next_facing == SOUTH: next_zone_pos = P(zone_pos.y, zone_pos.x)
                        if next_facing == WEST:  next_zone_pos = P(max_index - zone_pos.x, zone_pos.y)
                        if next_facing == EAST:  next_zone_pos = P(zone_pos.x, max_index - zone_pos.y)

                    if walker.facing == NORTH:
                        if next_facing == WEST:  next_zone_pos = P(max_index - zone_pos.y, max_index - zone_pos.x)
                        if next_facing == EAST:  next_zone_pos = P(zone_pos.y, zone_pos.x)
                        if next_facing == NORTH: next_zone_pos = P(zone_pos.x, max_index - zone_pos.y)
                        if next_facing == SOUTH: next_zone_pos = P(max_index - zone_pos.x, zone_pos.y)

                    next_pos = zone_to_map(zone_dim, next_zone, next_zone_pos)

                if next_pos in wall_map: continue

                path.append((walker.pos.x, walker.pos.y, walker.facing))
                walker.pos    = next_pos
                walker.facing = next_facing

        if cmd == 'L':
            walker.facing = (walker.facing + LEFT) % 4
        if cmd == 'R':
            walker.facing = (walker.facing + RIGHT) % 4

    adjusted_pos = sum_vecs(walker.pos, P(1, 1))
    return 1000 * adjusted_pos.y + 4 * adjusted_pos.x + walker.facing


if __name__ == '__main__':
    print("--------- Day 22 -----------")
    print(f"Part 1: { part_1(*prepare('input/day22.txt')) }")

    print("---------------------------")
    print(f"Part 2: { part_2(*prepare('input/day22.txt')) }")

#--------------------------------------------------------------------
import pytest

# --------------------------------------------------------------------------------------
# THIS ONLY WORKS FOR THE SAMPLE DATA, SO YAY
#                   2v
#                + - - +
#                |     |
#              v3|  1  |6<
#      1v    1>  |     |
#    + - - + - - + - - +
#    |     |     |     |
#  6^|  2  |  3  |  4  |6v
#    |     |     |     |  4<
#    + - - + - - + - - + - - +
#      5^    5>  |     |     |
#              3^|  5  |  6  |1<
#                |     |     |
#                + - - + - - +
#                  2^    2>
def map_to_zone(zone_dim, z, p):
    _map_to_zone = {
        1: lambda p: P(p.x - (2 * zone_dim), p.y - (0 * zone_dim)),
        2: lambda p: P(p.x - (0 * zone_dim), p.y - (1 * zone_dim)),
        3: lambda p: P(p.x - (1 * zone_dim), p.y - (1 * zone_dim)),
        4: lambda p: P(p.x - (2 * zone_dim), p.y - (1 * zone_dim)),
        5: lambda p: P(p.x - (2 * zone_dim), p.y - (2 * zone_dim)),
        6: lambda p: P(p.x - (3 * zone_dim), p.y - (2 * zone_dim)),
    }
    return _map_to_zone[z](p)

def zone_to_map(zone_dim, z, p):
    _zone_to_map = {
        1: lambda p: P(p.x + (2 * zone_dim), p.y + (0 * zone_dim)),
        2: lambda p: P(p.x + (0 * zone_dim), p.y + (1 * zone_dim)),
        3: lambda p: P(p.x + (1 * zone_dim), p.y + (1 * zone_dim)),
        4: lambda p: P(p.x + (2 * zone_dim), p.y + (1 * zone_dim)),
        5: lambda p: P(p.x + (2 * zone_dim), p.y + (2 * zone_dim)),
        6: lambda p: P(p.x + (3 * zone_dim), p.y + (2 * zone_dim)),
    }
    return _zone_to_map[z](p)

def zone_to_zone(from_facing, to_facing):
    to_zone = {
        1: {EAST: (6, WEST),  SOUTH: (4, SOUTH), WEST: (3, SOUTH), NORTH: (2, SOUTH)},
        2: {EAST: (3, EAST),  SOUTH: (5, NORTH), WEST: (6, NORTH), NORTH: (1, SOUTH)},
        3: {EAST: (4, EAST),  SOUTH: (5, EAST),  WEST: (2, WEST),  NORTH: (1, EAST)},
        4: {EAST: (6, SOUTH), SOUTH: (5, SOUTH), WEST: (3, WEST),  NORTH: (1, NORTH)},
        5: {EAST: (6, EAST),  SOUTH: (2, NORTH), WEST: (3, NORTH), NORTH: (4, NORTH)},
        6: {EAST: (1, WEST),  SOUTH: (2, EAST),  WEST: (5, WEST),  NORTH: (4, WEST)},
    }
    return to_zone[from_facing][to_facing]

def which_zone(zone_dim, p):
    col = p.x // zone_dim
    row = p.y // zone_dim
    lookup = [
        [0,0,1,0],
        [2,3,4,0],
        [0,0,5,6]
    ]
    zone = lookup[row][col]
    return zone
# EOM
# --------------------------------------------------------------------------------------

def test_prepare():
    zone_map, wall_map, commands = prepare('input/day22-example.txt')
    path = [(8,0,0),  (9,0,0),  (10,0,1),
            (10,1,1), (10,2,1), (10,3,1),
            (10,4,1), (10,5,0), (11,5,0),
            (0,5,0),  (1,5,0),  (2,5,0),
            (3,5,1),  (3,6,1),  (3,7,0),
            (4,7,0),  (5,7,0),  (6,7,0),
            (7,7,1),  (7,4,1)]
    print("\n" + render_map(zone_map, loc=P(7,5), path=path))
    print(wall_map)

def test_part_1():
    zone_map, wall_map, commands = prepare('input/day22-example.txt')
    assert part_1(zone_map, wall_map, commands) == 6032

def test_part_2():
    zone_map, wall_map, commands = prepare('input/day22-example.txt')
    assert part_2(zone_map, wall_map, commands) == 5031
