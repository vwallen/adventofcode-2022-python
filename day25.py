from more_itertools import collapse, pairwise, chunked

def to_dec(s):
    d = 0
    for i, n in enumerate(s[::-1]):
        if n.isdigit():
            d += int(n) * (5**i)
        elif n == '-':
            d += -1 * (5**i)
        elif n == '=':
            d += -2 * (5**i)
    return d

def to_snafu(d1):
    d2 = d1
    s = [0]

    for i in list(range(0,20))[::-1]:
        if d1 % 5**i == d1:
            continue
        d3 = d2 // 5**i
        d2 = d2 %  5**i
        if   d3 == 4: s.append((1,-1))
        elif d3 == 3: s.append((1,-2))
        else:         s.append((0, d3))

    s = [sum(pair) for pair in chunked(collapse(s),2)]

    for i, n in enumerate(s):
        if n == 3:
            s[i]   = -2
            s[i-1] = s[i-1] + 1

    if s[0] == 0: s.pop(0)
    for i, n in enumerate(s):
        if n == -1:   s[i] = '-'
        elif n == -2: s[i] = '='
        else:         s[i] = str(n)

    return ''.join(s)

def part_1(file_path):
    with open(file_path,'r') as infile:
       values = [to_dec(val) for val in infile.read().splitlines()]
    return to_snafu(sum(values))

if __name__ == '__main__':
    print("--------- Day 24 -----------")
    print(f"Part 1: { part_1('input/day25.txt') }")

#-----------------------------------------------------------------------
import pytest

def test_part_1():
    assert part_1('input/day25-example.txt') == '2=-1=0'