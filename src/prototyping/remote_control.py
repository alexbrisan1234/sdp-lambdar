#!/usr/bin/env python3
import curses
import ev3dev.ev3 as ev3

SPEED = 1050

def main(stdscr):
    left_f = ev3.LargeMotor('outB')
    left_r = ev3.LargeMotor('outC')
    right_f = ev3.LargeMotor('outA')
    right_r = ev3.LargeMotor('outD')
    curses.halfdelay(5)
    k = ''
    while k != 'Q' and k != 'q':
        if k == 'KEY_UP':
            left_f.run_forever(speed_sp=SPEED)
            left_r.run_forever(speed_sp=-SPEED)
            right_f.run_forever(speed_sp=SPEED)
            right_r.run_forever(speed_sp=-SPEED)
        if k == 'KEY_DOWN':
            left_f.run_forever(speed_sp=-SPEED)
            left_r.run_forever(speed_sp=SPEED)
            right_f.run_forever(speed_sp=-SPEED)
            right_r.run_forever(speed_sp=SPEED)
        if k == 'KEY_LEFT':
            left_f.stop()
            left_r.stop()
            right_f.run_forever(speed_sp=SPEED)
            right_r.run_forever(speed_sp=-SPEED)
        if k == 'KEY_RIGHT':
            left_f.run_forever(speed_sp=SPEED)
            left_r.run_forever(speed_sp=-SPEED)
            right_f.stop()
            right_r.stop()
        if k == '_NOTHING_':
            left_f.stop()
            left_r.stop()
            right_f.stop()
            right_r.stop()
        #stdscr.refresh()
        try:
            k = stdscr.getkey()
        except:
            k = '_NOTHING_'

curses.wrapper(main)

