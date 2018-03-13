#! /usr/bin/env python3
from motor import ArnoldMotors
from time import sleep


tr = 0
speed = 400
motors = ArnoldMotors({'frontLeft':'A','frontRight':'B','rearLeft':'C','rearRight':'D'}, speed)
motors.set_parameters(speed, tr)

while (tr < 1):
    motors.set_parameters(speed, tr)
    tr = tr + 0.1
    sleep(0.5)

while (tr > -1):
    motors.set_parameters(speed, tr)
    tr = tr - 0.1
    sleep(0.5)

speed = 0
while (speed < 1000):
    motors.set_parameters(speed, 1)
    speed = speed + 100
    sleep(0.5)

motors.stop()