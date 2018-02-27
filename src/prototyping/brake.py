#!/usr/bin/env python3
import curses
from motor import Motor

SPEED = 1050

def main(stdscr):
    m = ev3.LargeMotor('outA')
    curses.halfdelay(5)
    k = ''
    while k != 'Q' and k != 'q':
        if k == 'KEY_UP':
            m.run(1000, SPEED)
        if k == 'KEY_DOWN':
            pass
        if k == 'KEY_LEFT':
            pass
        if k == 'KEY_RIGHT':
            pass
        if k == '_NOTHING_':
            m.stop_free()
        try:
            k = stdscr.getkey()
        except:
            k = '_NOTHING_'

curses.wrapper(main)
