import parse
from operator import add, sub, mul, floordiv

class Monkey:
    def __init__(self, monkeys, uid, op, lhs=None, rhs=None):
        self.uid = uid
        self.monkeys = monkeys
        self.op = op
        self.lhs = lhs
        self.rhs = rhs
        self.caller = None
        
    def __repr__(self):
        return f"{self.uid}: {self.lhs}, {self.rhs}, {self.op}"
    
    def __call__(self):
        if self.lhs:
            return self.op(self.monkeys[self.lhs](), self.monkeys[self.rhs]())
        else:
            return self.op()

def yell(n):
    return lambda: n

def prepare(file_name):
    monkey_business = dict()
    with open(file_name, 'r') as infile:
        for line in infile.readlines():
            match = parse.search("{m:w}: {lhs:w} {op} {rhs:w}", line)
            if match is not None:
                m   = match['m']
                lhs = match['lhs']
                rhs = match['rhs']
                op  = match['op']
                if op == "+": op = add
                if op == "-": op = sub
                if op == "*": op = mul
                if op == "/": op = floordiv
                monkey_business[m] = Monkey(monkey_business, m, op, lhs, rhs)
                continue

            match = parse.search("{m:w}: {n:d}", line)
            if match is not None:
                m = match['m']
                n = match['n']
                monkey_business[m] = Monkey(monkey_business, m, yell(n),)

    for uid, monkey in monkey_business.items():
        if monkey.lhs is not None:
            monkey_business[monkey.lhs].caller = monkey
            monkey_business[monkey.rhs].caller = monkey

    return monkey_business

def part_1(monkeys):
    return monkeys['root']()

def part_2(monkeys):
    root = monkeys['root']
    humn = monkeys['humn']

    callers = list()
    caller = humn.caller
    while caller != root:
        callers.append(caller)
        caller = caller.caller

    def reverse_op(op, func, operand, left=False):
        if caller.op == sub:
            if left:
                return lambda n: func(sub(operand, n))
            else:
                return lambda n: func(add(n, operand))
        if caller.op == mul:
            revop = floordiv
        elif caller.op == floordiv:
            revop = mul
        else:
            revop = sub
        return lambda n: func(revop(n, operand))

    child = humn
    monkey_func = lambda n: n
    for caller in callers:
        if child.uid == caller.lhs:
            other = monkeys[caller.rhs]
            monkey_func = reverse_op(caller.op, monkey_func, other())
        else:
            other = monkeys[caller.lhs]
            monkey_func = reverse_op(caller.op, monkey_func, other(), left=True)
        child = caller

    answer = monkey_func(monkeys[root.rhs]())
    return answer

if __name__ == '__main__':
    print("--------- Day 21 -----------")
    print(f"Part 1: { part_1(prepare('input/day21.txt')) }")

    print("---------------------------")
    print(f"Part 2: { part_2(prepare('input/day21.txt')) }")

#-----------------------------------------------------------
import pytest

def test_part_1():
    assert part_1(prepare('input/day21-example.txt')) == 152

def test_part_2():
    assert part_2(prepare('input/day21-example.txt')) == 301