import pprint
import numpy as np
import parse
import math

pp = pprint.PrettyPrinter()

def mag(v):
    return np.sqrt(v.dot(v))
    
def vadd(v, n):
    m = mag(v)
    if m == 0:
        return v * 1
    return (m + n) * (v / m)

def mv(vec_h, vec_t, mv_h):
    vec_h = vec_h + mv_h
    mv_t = np.round(vadd(vec_h - vec_t, -1))
    vec_t = vec_t + mv_t
    return vec_h, vec_t

def walk(vec_a, vec_b):
    pp = []
    va = np.array([0,0])
    vb = vec_a - vec_b
    while not (va == vb).all():
        dm = mag(vb - va)
        if dm < 1.5:
            break
        vb = vb - np.round((vb - va)/dm)
        pp.append(vec_a + vb)
    return pp

#---------------------------------------------------------------

def prepare(file_path):
    with open(file_path, 'r') as infile:
        input = infile.read()

    moves = []
    for parsed in parse.findall("{cmd} {val:d}\n", input):
        cmd = parsed['cmd']
        val = parsed['val'] * 1.0
        moves.append({
            'R': np.array((val, 0.0)),
            'L': np.array((-val, 0.0)),
            'U': np.array((0.0, val)),
            'D': np.array((0.0, -val)),
        }[cmd])

    return moves

def part_1(moves):
    vec_h = np.array((0, 0))
    vec_t = np.array((0, 0))

    visited = {(0.0, 0.0),}
    for move in moves:
        vec_hn, vec_tn = mv(vec_h, vec_t, move)

        visited.add(tuple(vec_tn))
        for p in walk(vec_t, vec_tn):
            visited.add(tuple(p))

        vec_h = vec_hn
        vec_t = vec_tn

    return len(visited)

def part_2(moves):
    return 1

if __name__ == '__main__':
    moves = prepare('input/day09.txt')
    print("--------- Day 8 -----------")
    print("Part 1: %s" % part_1(moves))
    print("Part 2: %s" % part_2(moves))

#---------------------------------------------------------------
import pytest

@pytest.fixture
def moves():
    return prepare('input/day09-example.txt')

def test_part_1(moves):
    assert part_1(moves) == 13

def test_part_2(moves):
    assert part_2(moves) == 1
