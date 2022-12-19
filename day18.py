import parse
from itertools import product
from more_itertools import collapse
from collections import namedtuple, deque

Cube = namedtuple('Cube', ['x','y','z'])
Faces = namedtuple('Faces', ['xp','xq','yp','yq','zp','zq'])
Bounds = namedtuple('Bounds', ['min', 'max'])

def sum_cubes(a, b):
    return Cube(a.x + b.x, a.y + b.y, a.z + b.z)

def adjacent(cube):
    return (
        sum_cubes(cube, Cube(-1, 0, 0)),
        sum_cubes(cube, Cube( 1, 0, 0)),
        sum_cubes(cube, Cube( 0,-1, 0)),
        sum_cubes(cube, Cube( 0, 1, 0)),
        sum_cubes(cube, Cube( 0, 0,-1)),
        sum_cubes(cube, Cube( 0, 0, 1)),
    )

def update_faces(cubes):
    for cube in cubes:
        cubes[cube] = Faces(*map(lambda c: c not in cubes, adjacent(cube)))

def get_search_bounds(cubes):
    return Bounds(
        Cube(
            min(c.x for c in cubes.keys()) - 1,
            min(c.y for c in cubes.keys()) - 1,
            min(c.z for c in cubes.keys()) - 1,
        ),
        Cube(
            max(c.x for c in cubes.keys()) + 1,
            max(c.y for c in cubes.keys()) + 1,
            max(c.z for c in cubes.keys()) + 1,
        ),
    )

def get_bounds_checker(bounds):
    def _in_bounds(cube):
        return cube.x >= bounds.min.x and cube.x <= bounds.max.x and \
               cube.y >= bounds.min.y and cube.y <= bounds.max.y and \
               cube.z >= bounds.min.z and cube.z <= bounds.max.z
    return _in_bounds

#------------------------------------------------------------

def prepare(file_name):
    cubes = dict()
    with open(file_name,'r') as infile:
        for line in infile.readlines():
            coords = parse.search('{:d},{:d},{:d}', line)
            cubes[Cube(*coords)] = Faces(1,1,1,1,1,1)
    update_faces(cubes)
    return cubes

def part_1(cubes):
    all_faces = [faces for _, faces in cubes.items()]
    return sum(list(collapse(all_faces)))

def part_2(cubes):

    bounds = get_search_bounds(cubes)
    in_bounds = get_bounds_checker(bounds)

    volume = dict()
    for x in range(bounds.min.x, bounds.max.x + 1):
        for y in range(bounds.min.y, bounds.max.y + 1):
            for z in range(bounds.min.z, bounds.max.z + 1):
                volume[Cube(x, y, z)] = Faces(1,1,1,1,1,1)

    queue = deque()
    queue.append(Cube(bounds.min.x, bounds.min.y, bounds.min.z))
    searched = set()
    while queue:
        cursor = queue.popleft()
        searched.add(cursor)
        if cursor not in cubes:
            del volume[cursor]
        for adj in adjacent(cursor):
            if adj in searched:    continue
            if not in_bounds(adj): continue
            if adj not in queue and adj not in cubes:
                queue.append(adj)

    update_faces(volume)

    all_faces = [faces for _, faces in volume.items()]
    return sum(list(collapse(all_faces)))

if __name__ == '__main__':
    print("--------- Day 18 -----------")
    print(f"Part 1: { part_1(prepare('input/day18.txt')) }")

    print("---------------------------")
    print(f"Part 2: { part_2(prepare('input/day18.txt')) }")

#----------------------------------------------------------------
import pytest

@pytest.fixture
def cubes():
    return prepare('input/day18-example.txt')

def test_part_1(cubes):
    assert part_1(cubes) == 64

def test_part_2(cubes):
    assert part_2(cubes) == 58