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

def mv_both(vec_h, vec_t, mv_h):
    vec_h = vec_h + mv_h
    mov_t = np.round(vadd(vec_h - vec_t, -1))
    vec_t = vec_t + mov_t
    return vec_h, vec_t

def mv_tail(vec_h, vec_t, mv_h):
    mov_t = np.round(vadd(vec_h - vec_t, -1))
    vec_t = vec_t + mov_t
    return vec_t, mov_t

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
    visited = {(0.0, 0.0),}

    vec_h = np.array((0, 0))
    vec_t = np.array((0, 0))
    for move in moves:
        mna = max(abs(move))
        for _ in range(1, int(mna + 1)):
            mov_h = move/mna
            vec_h, vec_t = mv_both(vec_h, vec_t, mov_h)

            visited.add(tuple(vec_t))

    return len(visited)

def part_2(moves):

    visited = {(0.0, 0.0),}

    vec_h = np.array((0.0, 0.0))
    vecs_t = [np.array((0.0, 0.0)) for n in range(9)]
    for move in moves:
        mna = max(abs(move))
        for i in range(1, int(mna + 1)):
            mov_t = move/mna
            vec_h = vec_h + mov_t
            vec_th = vec_h
            for i, vec_t in enumerate(vecs_t):
                vec_th, mov_t = mv_tail(vec_th, vec_t, mov_t)
                vecs_t[i] = vec_th

            visited.add(tuple(vecs_t[8]))

    return len(visited)


if __name__ == '__main__':
    moves = prepare('input/day09.txt')
    print("--------- Day 8 -----------")
    print("Part 1: %s" % part_1(moves))
    print("Part 2: %s" % part_2(moves))

#---------------------------------------------------------------
import pytest

def test_part_1():
    moves = prepare('input/day09-example-1.txt')
    assert part_1(moves) == 13

def test_part_2():
    moves = prepare('input/day09-example-1.txt')
    assert part_2(moves) == 1
    moves = prepare('input/day09-example-2.txt')
    assert part_2(moves) == 36
