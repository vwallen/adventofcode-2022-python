from collections import namedtuple, deque, defaultdict

P = namedtuple('P', ['x', 'y'])
D = namedtuple('D', ['NE', 'N', 'NW', 'E', 'W', 'SE', 'S', 'SW'])

def sum_vecs(a, b):
    return P(a.x + b.x, a.y + b.y)

class Elf:
    def __init__(self, pos, elves):
        self.pos = pos
        self.elves = elves
        self.considerations = deque([
            self._consider_north,
            self._consider_south,
            self._consider_west,
            self._consider_east
        ])

    def _adjacent(self):
        return D(
            sum_vecs(self.pos, P( 1,-1)), # NE
            sum_vecs(self.pos, P( 0,-1)), # N
            sum_vecs(self.pos, P(-1,-1)), # NW
            sum_vecs(self.pos, P( 1, 0)), # E
            sum_vecs(self.pos, P(-1, 0)), # W
            sum_vecs(self.pos, P( 1, 1)), # SE
            sum_vecs(self.pos, P( 0, 1)), # S
            sum_vecs(self.pos, P(-1, 1)), # SW
        )

    def _find_elves(self, adj):
        found = D(
            self.elves.get(adj.NE),
            self.elves.get(adj.N),
            self.elves.get(adj.NW),
            self.elves.get(adj.E),
            self.elves.get(adj.W),
            self.elves.get(adj.SE),
            self.elves.get(adj.S),
            self.elves.get(adj.SW),
        )
        return len(list(filter(lambda e: e is not None, found))) == 0, found

    def _consider_north(self, found, adj):
        if found.NW: return
        if found.N:  return
        if found.NE: return
        return adj.N

    def _consider_south(self, found, adj):
        if found.SW: return
        if found.S:  return
        if found.SE: return
        return adj.S

    def _consider_west(self, found, adj):
        if found.NW: return
        if found.W:  return
        if found.SW: return
        return adj.W

    def _consider_east(self, found, adj):
        if found.NE: return
        if found.E:  return
        if found.SE: return
        return adj.E

    def think(self):
        adj = self._adjacent()
        empty, found = self._find_elves(adj)
        if not empty:
            for func in self.considerations:
                proposal = func(found, adj)
                if proposal is not None:
                    return proposal

    def think_again(self):
        self.considerations.append(self.considerations.popleft())

    def move(self, move_to):
        del self.elves[self.pos]
        self.pos = move_to
        self.elves[self.pos] = self

def prepare(file_name):
    elves = dict()
    with open(file_name, 'r') as infile:
        for y, row in enumerate(infile.read().splitlines()):
            for x, ch in enumerate(row):
                if ch == '#':
                    pos = P(x,y)
                    elves[pos] = Elf(pos, elves)
    return elves

def render_area(elves):
    x_min = min(pos.x for pos in elves.keys())
    x_max = max(pos.x for pos in elves.keys())
    y_min = min(pos.y for pos in elves.keys())
    y_max = max(pos.y for pos in elves.keys())
    out = "\n"
    for y in range(y_min, y_min + abs(y_max - y_min) + 1):
        for x in range(x_min, x_min + abs(x_max - x_min) + 1):
            elf = elves.get((x, y))
            if elf: out += "#"
            else:   out += "."
        out += "\n"
    return out

def do_moves(elves):
    moves = 0
    proposed = defaultdict(list)
    for _, elf in elves.items():
        prop = elf.think()
        if prop:
            proposed[prop].append(elf)
        elf.think_again()
    for prop, proposers in proposed.items():
        if len(proposers) > 1:
            continue
        proposers[0].move(prop)
        moves += 1
    return moves

def part_1(elves):
    for _ in range(10):
        do_moves(elves)
    x_min = min(pos.x for pos in elves.keys())
    x_max = max(pos.x for pos in elves.keys())
    y_min = min(pos.y for pos in elves.keys())
    y_max = max(pos.y for pos in elves.keys())
        
    return abs(x_max - x_min + 1) * abs(y_max - y_min + 1) - len(elves)

def part_2(elves):
    moves = 1
    rounds = 0
    while moves > 0:
        moves = do_moves(elves)
        rounds += 1
    return rounds

if __name__ == '__main__':
    print("--------- Day 23 -----------")
    print(f"Part 1: { part_1(prepare('input/day23.txt')) }")

    print("---------------------------")
    print(f"Part 2: { part_2(prepare('input/day23.txt')) }")

#------------------------------------------------------------
import pytest

def test_prepare():
    elves = prepare('input/day23-example.txt')
    assert elves[(4, 0)].pos == (4, 0)
    assert elves[(1, 5)].pos == (1, 5)
    assert elves.get((4, 5)) is None

def test_part_1():
    elves = prepare('input/day23-example.txt')
    empty_areas = part_1(elves)
    assert empty_areas == 110

def test_part_2():
    elves = prepare('input/day23-example.txt')
    rounds = part_2(elves)
    assert rounds == 20
