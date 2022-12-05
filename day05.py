def chunk(sequence, size):
    return [sequence[i : i+size] for i in range(0, len(sequence), size)]

def prepare(file_path):
    with open(file_path, 'r') as infile:
        input = infile.read()

    inventory_section, command_section = (section.split("\n") for section in input.split("\n\n"))

    inventory_section.reverse()
    inventory = [list() for _ in range(len(inventory_section[0][::4]))]
    for line in inventory_section[1:]:
        for col, crate in enumerate(chunk(line, 4)):
            item = crate[1:2].strip()
            if item != '':
                inventory[col].append(item)

    commands = []
    for line in command_section:
        if line.strip() != '':
            a, f, t = map(int, line.split(" ")[1::2])
            commands.append((f - 1, t - 1, a))

    return inventory, commands

def part_1(inventory, commands):
    for f, t, a in commands:
        for _ in range(a):
            inventory[t].append(inventory[f].pop())
    return "".join([stack[-1] for stack in inventory])

def part_2(inventory, commands):
    for f, t, a in commands:
        inventory[t] = inventory[t] + inventory[f][-a:]
        inventory[f] = inventory[f][:-a]
    return "".join([stack[-1] for stack in inventory])

if __name__ == '__main__':
    print("--------- Day 3 -----------")
    print("Part 1: %s" % part_1(*prepare('input/day05.txt')))
    print("Part 2: %s" % part_2(*prepare('input/day05.txt')))

#---------------------------------------------------------------
import pytest

def test_prepare_input():
    inventory, commands = prepare('input/day05-example.txt')
    assert ['Z', 'N'] == inventory[0]
    assert ['P'] == inventory[2]
    assert commands[0] == (1, 0, 1)
    assert commands[3] == (0, 1, 1)

def test_part_1():
    assert part_1(*prepare('input/day05-example.txt')) == 'CMZ'

def test_part_2():
    assert part_2(*prepare('input/day05-example.txt')) == 'MCD'
