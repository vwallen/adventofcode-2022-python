from collections import defaultdict
from pprint import PrettyPrinter

DIR = 0
FIL = 1

pp = PrettyPrinter()

def prepare(file_path):
    output = defaultdict(set)
    cwd = tuple()
    with open(file_path, 'r') as infile:
        for line in infile.read().splitlines():
            if line.startswith("$ ls"):
                continue # don't care
            elif line.startswith("$ cd"):
                _, _, arg = line.split(" ")
                if arg == "/":
                    cwd = tuple()
                elif arg == "..":
                    cwd = cwd[:-1]
                else:
                    cwd = cwd + (arg, )
            elif line.startswith("dir"):
                _, dirname = line.split(" ")
                output[cwd].add((DIR, cwd + (dirname, )))
            else:
                size, filename = line.split(" ")
                output[cwd].add((FIL, filename, int(size)))
    return output

def calc_size_recursive(root, path):
    files = 0
    dirs = 0
    node = root.get(path)
    if node is not None:
        for obj in node:
            if obj[0] == FIL:
                files += obj[2]
            else:
                dirs += calc_size_recursive(root, obj[1])
    return files + dirs

def part_1(root):

    totals = {}
    for d in root.keys():
        totals[d] = calc_size_recursive(root, d)
   
    targets = [v for k, v in totals.items() if v <= 100000]
    return sum(targets)

def part_2(root):
    disk_size = 70000000
    available_space = disk_size - calc_size_recursive(root, ())
    needed_space = 30000000 - available_space

    totals = {}
    for d in root.keys():
        totals[d] = calc_size_recursive(root, d)
    
    targets = [v for k, v in totals.items() if v > needed_space]
    targets.sort()
    return targets[0]

if __name__ == '__main__':
    input = prepare('input/day07.txt')
    print("--------- Day 7 -----------")
    print("Part 1: %s" % part_1(input))
    print("Part 2: %s" % part_2(input))

#---------------------------------------------------------------
import pytest

@pytest.fixture
def example():
    return prepare('input/day07-example.txt')

def test_part_1(example):
    assert part_1(example) == 95437

def test_part_2(example):
    assert part_2(example) == 24933642
