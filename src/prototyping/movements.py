#!/usr/bin/env python3
import curses
import ev3dev.ev3 as ev3

def __send_run_command_to_motors(motor_list, duration, speed):
    for motor in motor_list:
        print('sending command')
        motor . run_timed(time_sp = duration, speed_sp = speed)


def __send_stop_command_to_motors(motor_list):
    for motor in motor_list:
        motor . stop()

def MOVE_LEFT(device, duration, speed):
    __send_stop_command_to_motors(device['motors']['left'])
    __send_run_command_to_motors(device['motors']['right'], duration, speed)

def MOVE_RIGHT(device, duration, speed):
    __send_stop_command_to_motors(device['motors']['right'])
    __send_run_command_to_motors(device['motors']['right'], duration, speed)
    
def MOVE_FORWARDS(device, duration, speed):
    __send_run_command_to_motors(device['motors']['right'] + device['motors']['left'], duration, speed)

def MOVE_BACKWARDS(device, duration, speed):
    MOVE_FORWARDS(device, duration, -1 * speed)

def main(stdscr):
    left = ev3.LargeMotor('outB')
    right = ev3.LargeMotor('outC')

    curses . halfdelay(5)

    device = {
        'motors': {
            'left': [left],
            'right': [right]
        }
    }

    MOVE_FORWARDS(device, 3000, 500)




curses.wrapper(main)
