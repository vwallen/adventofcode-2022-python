import parse
from collections import namedtuple
from more_itertools import chunked

P = namedtuple('P', ['x', 'y'])
S = namedtuple('S', ['pos', 'beacon'])

class Span:
    def __init__(self, min, max):
        self.min = min
        self.max = max

    def __repr__(self):
        return f"{{{self.min}-{self.max}}}"

    def contains(self, n):
        return self.min <= n and n  <= self.max

class Coverage:
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r
        self.extent_x = Span(x - r, x + r)
        self.extent_y = Span(y - r, y + r)

    def covers_y(self, y):
        return self.extent_y.contains(y)

    def row(self, y):
        if self.covers_y(y):
            dist = abs(self.y - y)
            x = abs(self.r - dist)
            span = Span(self.x - x, self.x + x)
            return span

def prepare(file_name):
    with open(file_name, 'r') as infile:
        sensors = dict()
        for line in infile.read().splitlines():
            matches = parse.search("Sensor at x={sx:d}, y={sy:d}: closest beacon is at x={bx:d}, y={by:d}", line)
            sx, sy, bx, by = matches['sx'], matches['sy'], matches['bx'], matches['by']
            sensor = S(P(sx, sy), P(bx, by))
            sensors[sensor.pos] = sensor
    return sensors

def coverage_for(sensor):
    r = abs(sensor.pos.x - sensor.beacon.x) + abs(sensor.pos.y - sensor.beacon.y)
    return Coverage(sensor.pos.x, sensor.pos.y, r)

def part_1(scan_row, sensors, limits=None):

    spans = list()
    for _, sensor in sensors.items():
        coverage = coverage_for(sensor)
        span = coverage.row(scan_row)
        if span:
            spans.append((span.min, 0))
            spans.append((span.max, 2))

    spans.sort()
    x_min = spans[ 0][0]
    x_max = spans[-1][0]

    cursor = 0
    state  = 0
    gaps  = list()
    while spans:
        cursor, val = spans.pop(0)
        state += 1 - val
        if state > 0:
            if len(gaps) % 2 == 1:
                gaps.append(cursor)
        else:
            gaps.append(cursor)
    
    found_sensors = list()
    for gap in chunked(gaps, 2):
        if len(gap) == 2:
            if limits.contains(gap[0]) and limits.contains(gap[1]):
                for n in range(1, gap[1] - gap[0]):
                    found_sensors.append(P(gap[0] + n, scan_row))

    return x_max - x_min - len(found_sensors), found_sensors

def part_2(sensors, limits):

    for y in range(limits.min, limits.max + 1):
        # go in reverse because of course 
        # it will be nearer the bottom
        scan_row = limits.max - y
        _, found_sensors = part_1(scan_row, sensors, limits)
        if found_sensors:
            break

    sensor = found_sensors.pop()

    return sensor.x * 4_000_000 + sensor.y, sensor


if __name__ == '__main__':
    sensors = prepare('input/day15.txt')
    print("--------- Day 15 -----------")
    print(f"Part 1: { part_1(2000000, sensors) }")

    print("---------------------------")
    print(f"Part 2: { part_2(sensors, limits=Span(0, 4_000_000)) }")

#------------------------------------------------------------------
import pytest

@pytest.fixture
def sensors():
    return prepare('input/day15-example.txt')

def test_part_1(sensors):
    empty, sensors = part_1(10, sensors)
    assert empty == 26

def test_part_2(sensors):
    frequency, found_sensor = part_2(sensors, limits=Span(0, 20))
    assert frequency == 56000011

