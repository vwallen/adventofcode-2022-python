from curses import *
from math import ceil, floor
import pprint
import parse
import time

pp = pprint.PrettyPrinter()


def get_cycles(file_path):
    with open(file_path,'r') as infile:
        cycles = []
        for line in infile.readlines():
            cycles.append(0)
            op = parse.search("addx {addx:d}", line)
            if op is not None:
                cycles.append(op['addx'])
    return cycles

def get_signals(cycles):
    signal_strength = 0
    signal_strengths = []
    x_register = 1
    for c, signal in enumerate(cycles):
        cycle = c + 1
        if cycle in (20, 60, 100, 140, 180, 220):
            signal_strength = cycle * x_register
        signal_strengths.append(signal_strength)
        x_register += signal
    return signal_strengths

def get_pixels(cycles):
    pattern = [0] * 240
    x_register = 1
    for cycle, signal in enumerate(cycles):
        beam_col = cycle % 40
        pixl_col = x_register
        if abs(beam_col - pixl_col) < 2:
            pattern[cycle] = 1
        x_register += signal
    return pattern

def main(stdscr):
    cycles = get_cycles('input/day10.txt')
    signals = get_signals(cycles)
    pixels = get_pixels(cycles)

    #--------------------------------------------
    # everthing blow this line is cursed code
    # it will crash if your terminal window is
    # not at least 30 lines tall
    #--------------------------------------------

    curs_set(0)

    init_color(0, 0, 0, 0)

    init_color(1, 10, 60, 10)

    init_color(2, 250,  0, 0)
    init_color(3, 500,  0, 0)
    init_color(4, 750,  0, 0)
    init_color(5, 1000, 0, 0)

    init_color(6,  0, 100,  0)
    init_color(7,  0, 250,  0)
    init_color(8,  0, 400,  0)
    init_color(9,  0, 750,  0)
    init_color(10, 0, 1000, 0)

    init_pair(1, 3, 1) # frames colors
    init_pair(2, 4, 1) # signal colors
    init_pair(3, 5, 1) # registr graph
    init_pair(4, 4, 0) # signal graph
    init_pair(5, 7, 0) # display empty
    init_pair(6, 8, 0) # display low
    init_pair(7, 9, 0) # display mid
    init_pair(8, 10, 0) # display high

    stdscr.clear()
    # draw boxes
    # ╔═╗  ╬╦
    # ║ ║ ╠╩╣  │┤┐└┴┬├─┼┘┌ ░▒▓█
    # ╚═╝
    frames = """                                                        
       ╔═══════════════╗                                
     ╔═╣ ÆlfComms-3000 ╠══════════════════════════╗     
     ║ ╚═══════════════╝ cycle:                   ║     
     ║ ┌────────────────────────────────────────┐ ║     
     ║ ├                                        ┤ ║     
     ║ ├                                        ┤ ║     
     ║ ├                                        ┤ ║     
     ║ ├                                        ┤ ║     
     ║ ├                                        ┤ ║     
     ║ ├                                        ┤ ║     
     ║ ├                                        ┤ ║     
     ║ ├                                        ┤ ║     
     ║ ├                                        ┤ ║     
     ║ ├  ┌───────┐           ┌──────────────┐  │ ║     
     ║ └──┤X:░░░░ ├───────────┤signal: ░░░░░ ├──┘ ║     
     ║    └───────┘           └──────────────┘    ║     
     ╠════════════════════════════════════════════╣     
     ║ ┌────────────────────────────────────────┐ ║     
     ║ │                                        │ ║     
     ║ │                                        │ ║     
     ║ │                                        │ ║     
     ║ │                                        │ ║     
     ║ │                                        │ ║     
     ║ │                                        │ ║     
     ║ └────────────────────────────────────────┘ ║     
     ╚════════════════════════════════════════════╝    
                                                         
"""

    for y, f in enumerate(frames.splitlines()):
        stdscr.addstr(y, 0, f, color_pair(1))
    stdscr.refresh()

    graph = newpad(9, 240)

    for i, sig in enumerate(cycles):
        y = 3 - floor(sig/9)
        graph.addch(y, i, "│", color_pair(2))

    bucket = ceil(max(signals)/9)
    for i, sig in enumerate(signals):
        y = 8 - (sig//bucket)
        graph.addch(y, i, "▒", color_pair(8))


    cursor = 0
    signal_strength = set()
    while True:
        # display numbers
        if signals:
            signal_strength.add(signals.pop(0))
            signal = sum(signal_strength)
            stdscr.addstr(15, 38, f"{signal: >6} ", color_pair(6))    
        else:
            stdscr.addstr(15, 38, f"{signal: >6}", color_pair(7))    
            if 0 < cursor % 10  < 5:
                stdscr.addstr(15, 38, f"       ", color_pair(7))    
        register = cycles[cursor % len(cycles)]
        stdscr.addstr( 3, 31, f"{cursor: >4} ", color_pair(6))    
        stdscr.addstr(15, 13, f"{register: >+3} ", color_pair(6))

        #display register graph
        graph.refresh(0, cursor % 240, 5, 8, 13, 47)

        # dislay dispaly sweeper
        for n, px in enumerate(pixels):
            ch = '▒' if px else '░'
            y = 19 + (n//40)
            x = 8 + (n % 40)
            if (cursor % 40) == (n % 40):
                ch = "│"
                clr = color_pair(8)
            elif px and ((n % 40) + 3 >= (cursor % 40) >= (n % 40) + 1):
                clr = color_pair(8)
            elif px and ((n % 40) + 6 >= (cursor % 40) >= (n % 40) + 4):
                clr = color_pair(7)
            elif px and ((n % 40) + 12 >= (cursor % 40) >= (n % 40) + 7):
                clr = color_pair(6)
            else:
                clr = color_pair(5)
            stdscr.addstr(y, x, ch, clr)

        stdscr.refresh()
        time.sleep(0.025)
        cursor = (cursor + 1) % len(cycles)


if __name__ == '__main__':
    wrapper(main)

#---------------------------------------------------------------
import pytest

def test_part_1():
    cycles = get_cycles('input/day10.txt')
    assert sum(set(get_signals(cycles))) == 17180

def test_part_2():
    cycles = get_cycles('input/day10-example.txt')
    pattern = "".join(map(lambda x: "#" if x else ".", get_pixels(cycles)))
    assert pattern == "##..##..##..##..##..##..##..##..##..##..###...###...###...###...###...###...###.####....####....####....####....####....#####.....#####.....#####.....#####.....######......######......######......###########.......#######.......#######....."
