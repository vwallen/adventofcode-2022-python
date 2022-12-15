import math
from string import ascii_lowercase as elevations
from collections import namedtuple, deque, defaultdict
from more_itertools import pairwise, flatten

L = namedtuple('P', ['x', 'y'])              # a location position
E = namedtuple('E', ['code', 'elev'])        # a location elevation
D = namedtuple('D', ['N', 'S', 'W', 'E'])    # adjacent coords
M = namedtuple('M', ['elev', 'loc', 'step']) # a potential move

def prepare(file_path):
    elevation_map = defaultdict()
    start, goal = None, None
    with open(file_path, 'r') as infile:
        for y, row in enumerate(infile.read().splitlines()):
            for x, ch in enumerate(row):
                pt = L(x, y)
                if ch == 'S':
                    elevation_map[pt] = E('a', elevations.index('a'))
                    start = pt
                elif ch == 'E':
                    elevation_map[pt] = E('z', elevations.index('z'))
                    goal = pt
                else:
                    elevation_map[pt] = E(ch, elevations.index(ch))
    return elevation_map, start, goal

def scan(elevation_map, start, valid_move):

    distances = defaultdict(lambda: math.inf)
    distances[start] = 0

    searched = set()
    search_queue = deque([M(elevation_map[start], start, 0)])

    while search_queue:

        elevation, cursor, step = search_queue.popleft()
        next_step = step + 1

        adjacent = D(
            L(cursor.x, cursor.y - 1), # N
            L(cursor.x, cursor.y + 1), # S
            L(cursor.x + 1, cursor.y), # E
            L(cursor.x - 1, cursor.y), # W
        )
        possible_moves = list()
        for adj in adjacent:
            if adj not in searched and valid_move(cursor, adj):
                adj_steps = distances[adj]
                if next_step < adj_steps:
                    possible_moves.append(M(elevation_map[adj].elev, adj, next_step))
                    distances[adj] = next_step

        search_queue.extendleft(possible_moves)
            
    return distances

def part_1(elevation_map, start, goal):
    def move_validator(a, b):
        # only moves to and from valid locations
        if a in elevation_map and b in elevation_map:
            # only moves no more than 1 above current position
            if elevation_map[b].elev - elevation_map[a].elev < 2:
                return True
        return False
    distances = scan(elevation_map, start, move_validator)
    return distances[goal]

def part_2(elevation_map, start):
    def move_validator(a, b):
        # only moves to and from valid locations
        if a in elevation_map and b in elevation_map:
            # only moves no more than 1 below current position
            if elevation_map[a].elev - elevation_map[b].elev < 2:
                return True
        return False
    distances = scan(elevation_map, start, move_validator)
    return min(dist for loc, dist in distances.items() if elevation_map[loc].code == 'a')


if __name__ == '__main__':
    print("--------- Day 12 -----------")
    elevation_map, start, goal = prepare('input/day12.txt')
    print("Part 1: %s" % part_1(elevation_map, start, goal))

    print("----------------------------")
    elevation_map, _, start = prepare('input/day12.txt')
    print("Part 2: %s" % part_2(elevation_map, start))
    
#-------------------------------------------------------------
import pytest

def test_prepare():
    #     0 1 2 3 4 5 6 7
    #   +----------------
    # 0 | S a b q p o n m
    # 1 | a b c r y x x l
    # 2 | a c c s z E x k
    # 3 | a c c t u v w j
    # 4 | a b d e f g h i
    elevation_map, start, goal = prepare('input/day12-example.txt')
    assert start == (0, 0)
    assert goal  == (5, 2)
    assert elevation_map[start] == ('a', 0)
    assert elevation_map[goal]  == ('z', 25)

def test_part_1():
    elevation_map, start, goal = prepare('input/day12-example.txt')
    steps = part_1(elevation_map, start, goal)
    assert steps == 31

def test_part_2():
    elevation_map, goal, start = prepare('input/day12-example.txt')
    steps = part_2(elevation_map, start)
    assert steps == 29
