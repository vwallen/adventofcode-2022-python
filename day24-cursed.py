from curses import *
from day24 import *
import time
import random

def main(stdscr):
    
    w, h, winds = prepare('input/day24.txt')
    scout_map = dict()
    start = P(0, -1)
    goal  = P(w - 1, h)

    with open('input/day24-frame.txt', 'r') as infile:
        frame = infile.read()
    
    init_color(0, 0, 0, 0)          # black
    init_color(1, 1000, 200, 300) # 

    init_color(2, 600, 600, 1000)  # north wind
    init_color(3, 400, 800, 1000)  # south wind
    init_color(4, 0,   800, 1000)  # west wind
    init_color(5, 0,   1000, 1000) # east wind
    init_color(6, 250, 250, 250) # wall 1
    init_color(7, 200, 200, 200) # wall 2
    init_color(8,  250, 1000, 0)
    init_color(9,  800, 1000, 0)
    init_color(10, 800, 800,  0)

    init_pair(1, 1, 0) # frame colors
    init_pair(2, 2, 0) # N
    init_pair(3, 3, 0) # S
    init_pair(4, 4, 0) # W
    init_pair(5, 5, 0) # E
    init_pair(6, 6, 0)
    init_pair(7, 7, 0)
    init_pair(8, 8, 0)
    init_pair(9, 9, 0)
    init_pair(10, 10, 0)

    curs_set(0)
    stdscr.clear()
    for y, f in enumerate(frame.splitlines()):
        stdscr.addstr(y, 0, f, color_pair(1))
    stdscr.refresh()

    display_map = newpad(37, 103)

    for tick in navigate_to(w, h, winds, start, goal, scout_map):

        stdscr.addstr(3, 28, f"{tick:0>3}", color_pair(8))
        stdscr.refresh()

        locations = render_map(w, h, winds, scout_map.keys())
        for y, line in enumerate(locations.splitlines()):
            for x, ch in enumerate(line):
                color = color_pair(1)
                if ch == '^': color = color_pair(2)
                if ch == 'v': color = color_pair(3)
                if ch == '<': color = color_pair(4)
                if ch == '>': color = color_pair(5)
                if ch == '@':
                    color = color_pair(10)
                    dist = abs(x - goal.x) + abs(y - goal.y)
                    if dist < 100:
                        color = color_pair(9)
                    if dist < 50:
                        color = color_pair(8)
                if ch == '.': ch = ' '
                if ch == '#': 
                    ch = '█'
                    color = color_pair(6 + ((y+ x) % 2))

                display_map.addstr(y, x, ch, color)
        display_map.refresh(0, 0, 5, 2, 60, 103)

    stdscr.addstr(3, 28, f"{tick:0>3} COMPLETE!", color_pair(8))
    stdscr.refresh()
    while True:
        pass

if __name__ == '__main__':
    wrapper(main)
