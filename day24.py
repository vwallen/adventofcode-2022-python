from collections import namedtuple, defaultdict

P = namedtuple('P', ['x', 'y'])
A = namedtuple('D', ['N', 'S', 'E', 'W'])

NORTH = P( 0,-1)
SOUTH = P( 0, 1)
EAST  = P( 1, 0)
WEST  = P(-1, 0)

def sum_vecs(a, b):
    return P(a.x + b.x, a.y + b.y)

def adjacent(loc):
    return A(
        sum_vecs(loc, NORTH),
        sum_vecs(loc, SOUTH),
        sum_vecs(loc, EAST),
        sum_vecs(loc, WEST),
    )

class Scout:
    def __init__(self, loc, dist):
        self.loc = loc
        self.dist = dist

    def __repr__(self):
        return f"{self.loc}: {self.dist}"

def move_blizzards(w, h, winds):
    for i, wind in enumerate(winds.N):
        wind = sum_vecs(wind, NORTH)
        if wind.y < 0: wind = P(wind.x, h - 1)
        winds.N[i] = wind
    for i, wind in enumerate(winds.S):
        wind = sum_vecs(wind, SOUTH)
        if wind.y == h: wind = P(wind.x, 0)
        winds.S[i] = wind
    for i, wind in enumerate(winds.W):
        wind = sum_vecs(wind, WEST)
        if wind.x < 0: wind = P(w - 1, wind.y)
        winds.W[i] = wind
    for i, wind in enumerate(winds.E):
        wind = sum_vecs(wind, EAST)
        if wind.x == w: wind = P(0, wind.y)
        winds.E[i] = wind

def render_map(w, h, winds, scouts):
    out = ""
    for y in range(-1, h + 1):
        for x in range(-1, w + 1):
            p = P(x, y)
            if   p in scouts:     out += "@"
            elif p in winds.N:    out += "^"
            elif p in winds.S:    out += "v"
            elif p in winds.W:    out += "<"
            elif p in winds.E:    out += ">"
            elif p == (0, -1):    out += " "
            elif p == (w-1, h):   out += " "
            elif x == w or x < 0: out += "#"
            elif y == h or y < 0: out += "#"
            else: out += "."
        out += "\n"
    return out

def prepare(file_path):
    north_wind = list()
    south_wind = list()
    west_wind  = list()
    east_wind  = list()
    with open(file_path, 'r') as infile:
        lines = infile.read().splitlines()
    lines = lines[1:-1]
    for y, line in enumerate(lines):
        line = line[1:-1]
        for x, ch in enumerate(line):
            if ch == '^': north_wind.append(P(x, y))
            if ch == 'v': south_wind.append(P(x, y))
            if ch == '>': east_wind.append(P(x, y))
            if ch == '<': west_wind.append(P(x, y))
    w, h = len(line), len(lines)
    return w, h, A(north_wind, south_wind, east_wind, west_wind)

def navigate_to(w, h, winds, start, goal, scout_map=None):

    if scout_map is None: scout_map = dict()
    scout_map[start] = Scout(start, 0)

    tick = 0
    while True:
        tick += 1

        # place scouts
        new_recruits = list()
        for loc, scout in scout_map.items():
            scout.dist = tick
            for adj in adjacent(loc):
                if adj == goal:
                    new_recruits.append(Scout(adj, tick))
                    continue
                if adj.x < 0 or adj.x == w: continue
                if adj.y < 0 or adj.y == h: continue
                new_recruits.append(Scout(adj, tick))
        for scout in new_recruits:
            scout_map[scout.loc] = scout

        move_blizzards(w, h, winds)

        # remove scouts
        for wind in winds:
            for blizzard in wind:
                if blizzard in scout_map:
                    del scout_map[blizzard]

        yield tick
        if goal in scout_map.keys():
            break


def part_1(w, h, winds):

    start = P(0, -1)
    goal  = P(w - 1, h)
    return list(navigate_to(w, h, winds, start, goal)).pop()

def part_2(w, h, winds):

    start = P(0, -1)
    goal  = P(w - 1, h)
    leg_1 = list(navigate_to(w, h, winds, start, goal)).pop()
    leg_2 = list(navigate_to(w, h, winds, goal, start)).pop()
    leg_3 = list(navigate_to(w, h, winds, start, goal)).pop()

    return leg_1 + leg_2 + leg_3

if __name__ == '__main__':
    print("--------- Day 24 -----------")
    print(f"Part 1: { part_1(*prepare('input/day24.txt')) }")

    print("---------------------------")
    print(f"Part 2: { part_2(*prepare('input/day24.txt')) }")


#-------------------------------------------------------
import pytest

def test_prepare():
    w, h, winds = prepare('input/day24-example.txt')
    assert (4, 0) in winds.N
    assert (2, 3) in winds.S
    assert (5, 2) in winds.E
    assert (0, 3) in winds.W

def test_part_1():
    w, h, winds = prepare('input/day24-example.txt')
    assert part_1(w, h, winds) == 18

def test_part_2():
    w, h, winds = prepare('input/day24-example.txt')
    assert part_2(w, h, winds) == 54
