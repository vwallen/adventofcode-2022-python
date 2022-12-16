import parse
from collections import namedtuple
from math import cos, sin
from math import pi as PI
from more_itertools import flatten
from itertools import combinations, product
from functools import partial, reduce
from operator import or_

P = namedtuple('P', ['x', 'y'])                    # a point
S = namedtuple('S', ['p', 'q'])                    # a span
Z = namedtuple('Z', ['px', 'qx', 'py', 'qy', 'r']) # a zone

def prepare(file_name):
    with open(file_name, 'r') as infile:
        zones = list()
        for line in infile.read().splitlines():
            matches = parse.search("Sensor at x={sx:d}, y={sy:d}: closest beacon is at x={bx:d}, y={by:d}", line)
            sx, sy, bx, by = matches['sx'], matches['sy'], matches['bx'], matches['by']
            sensor = P(sx, sy)
            beacon = P(bx, by)
            radius = abs(sensor.x - beacon.x) + abs(sensor.y - beacon.y)
            zones.append(Z(
                P(sensor.x - radius, sensor.y),
                P(sensor.x + radius, sensor.y),
                P(sensor.x, sensor.y - radius),
                P(sensor.x, sensor.y + radius),
                radius
            ))
    return zones

def span_contains(span, n):
    return span.p <= n and n  <= span.q

def span_x(zone, y):
    if span_contains(S(zone.py.y, zone.qy.y), y):
        d = abs(zone.px.y - y)
        x = abs(zone.r - d)
        return S(zone.py.x - x, zone.py.x + x)

def zone_contains(zone, p):
    d = abs(zone.py.x - p.x) + abs(zone.px.y - p.y)
    return d <= zone.r

def rotate_point(radians, p):
    x = round( p.x * cos(radians) + p.y * sin(radians))
    y = round(-p.x * sin(radians) + p.y * cos(radians))
    return P(x, y)
right_45 = partial(rotate_point,  PI/4)
left_45  = partial(rotate_point, -PI/4)

def part_1(zones, scan_row):
    # if the zones are contiguous in this row, all points
    # from lowest to highest are included in the answer
    all_spans = list(filter(lambda n: n is not None, [span_x(z, scan_row) for z in zones]))
    all_points = list(flatten(all_spans))
    return max(all_points) - min(all_points)

def part_2(zones, limits):

    # get the min/max points of the sensor coverage zones
    # rotate them 45° to convert the sensor zones into AABBs
    # collect unique x and y values
    all_points  = list(flatten(z[:-1] for z in zones))
    all_rotated = list(map(right_45, all_points))
    all_x = list(set(p.x for p in all_rotated))
    all_y = list(set(p.y for p in all_rotated))

    # find all of the x and y values within
    # two positions of each other, and
    # get the value between them
    find_near_x = lambda a: abs(a[0] - a[1]) <= 2
    find_near_y = lambda a: abs(a[0] - a[1]) <= 2
    near_mid    = lambda a: 0.5 * abs(max(a) - min(a)) + min(a)
    near_x = list(filter(find_near_x, combinations(all_x, 2)))
    near_y = list(filter(find_near_y, combinations(all_y, 2)))
    found_x = list(map(near_mid, near_x))
    found_y = list(map(near_mid, near_y))

    # make points out of every combo x,y of the 
    # found midpoints and rotate those 45° degrees
    # back to the original coord space
    found_points = [P(x, y) for x, y in product(found_x, found_y)]
    maybe_beacons = list(map(left_45, found_points))    

    # throw out any of those points
    # in an existing sensor zone
    # take the last one (of one, hopefully)
    out_of_zones = lambda p: not reduce(or_, (zone_contains(z, p) for z in zones))
    definitely_a_beacon = list(filter(out_of_zones, maybe_beacons)).pop()

    # if you found one, it's a beacon!
    if definitely_a_beacon:    
        return definitely_a_beacon.x * 4_000_000 + definitely_a_beacon.y

if __name__ == '__main__':
    zones = prepare('input/day15.txt')
    print("--------- Day 15 -----------")
    print(f"Part 1: { part_1(zones, 2_000_000) }")
    print("---------------------------")
    print(f"Part 2: { part_2(zones, limits=S(0, 4_000_000)) }")

#------------------------------------------------------------------
import pytest

@pytest.fixture
def zones():
    return prepare('input/day15-example.txt')

def test_rotate_point(zones):
    p0 = P(14, 11)
    p1 = right_45(p0)
    p2 = left_45(p1)
    assert p0 == p2

    p0 = P(3_335_216, 3_187_704)
    p1 = right_45(p0)
    p2 = left_45(p1)
    assert p0 == p2

def test_contains(zones):
    point = P(14, 11)
    contains = reduce(or_, (zone_contains(z, point) for z in zones))
    assert contains == False

    point = P(2, 10)
    contains = reduce(or_, (zone_contains(z, point) for z in zones))
    assert contains == True

def test_part_1(zones):
    assert part_1(zones, 10) == 26

def test_part_2(zones):
    assert part_2(zones, limits=S(0, 20)) == 56000011

