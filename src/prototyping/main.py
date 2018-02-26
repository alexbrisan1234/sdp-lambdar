#! /usr/bin/python3
from comms import Serial_Comm
from enum import Enum
from motor import *
from pid import PID
import time

class Arnold:
    # Arnold's to main sensory inputs
    ultra_data = None
    infra_data = None

    class Mode(Enum):
        FOLLOW = 1
        OBSTACLE = 2

    def __init__(self, cs=200, dur=5000):
        self.motors = ArnoldMotors({'frontLeft':'A','frontRight':'B','rearLeft':'C','rearRight':'D'});
        self.acting_mode = self.Mode.FOLLOW
        self.ser = Serial_Comm()
        self.pid = PID(P=0.5, I=0.0, D=0.0)
        self.constant_speed = cs
        self.left_speed = cs
        self.right_speed = cs
        self.duration = dur
        self.obstacle_position = 0 # 0 for left, 1 for right
        self.obstacle_distance = 0
        self.pid_output = 0.00

    def live(self):
        'Main loop of Arnold. Updates model and perform motions'
        while True:
            try:
                print('Getting Message')
                new_data = self.ser.read_message()

                if new_data[0] != None:
                    self.ultra_data = new_data[0]

                if new_data[1] != None:
                    self.ultra_data = new_data[1]

                print(self.ultra_data)
                
                # If the data from the ultrasonics is old then switch modes
                if self.ultra_data != None and int(round(time.time() * 1000)) - self.ultra_data.timestamp > 1000:
                    self.acting_mode = self.Mode.OBSTACLE
                else:
                    self.acting_mode = self.Mode.FOLLOW
                self.acting_mode = self.Mode.FOLLOW

                # Update motion based on current
                self.actuate()
            except KeyboardInterrupt:
                print('Aborting Robot Operation')
                break


    def actuate(self):
        'Logic for selecting an actuation strategy and activating motors'
        if self.acting_mode == self.Mode.FOLLOW:
            # get the pid output to tune the speed and direction
            self.pid_output = self.pid.update_tracking(self.ultra_data.get_left(),
                                                       self.ultra_data.get_right(),
                                                       self.ultra_data.timestamp)
            # turn left, allow for a small mistake
            '''if(pid_output>0.0001):
                self.left_speed = pid_output*self.constant_speed
                self.right_speed = self.constant_speed
                self.motors.turn(self.duration, self.left_speed, self.right_speed)
            elif(pid_output<-0.0001):
                # turn right
                self.right_speed = -pid_output*self.constant_speed
                self.left_speed = self.constant_speed
                self.motors.turn(self.duration, self.left_speed, self.right_speed)
                # if the error is *almost* corrected
            else: 
                self.motors.move_forwards(self.constant_speed, self.constant_speed)#'''
            spd_left = self.constant_speed + self.pid_output/2.0
            spd_right = self.constant_speed - self.pid_output/2.0
            if spd_left > 1000:
                spd_left = 1000
            if spd_left < -1000:
                spd_left = -1000
            if spd_right > 1000:
                spd_right = 1000
            if spd_right < -1000:
                spd_right = -1000
            self.motors.turn(self.duration, spd_left, spd_right)
            
        else:
            # check which side of the wall you're at, assume the robot is moving straight
            if(self.infra_data[2]!=0): # right sensor from arnold's perspective
                self.obstacle_position = 1
                self.obstacle_distance = self.infra_data[2]
                self.motors.move_forwards(self.constant_speed, self.constant_speed) 
            elif(self.infra_data[6]!=0): 
                self.obstacle_position = 0    
                self.obstacle_distance = self.infra_data[6]
                self.motors.move_forwards(self.constant_speed, self.constant_speed)
            # if readings from both sides are 0 and obstacle was on the left side   
            elif(self.obstacle_position == 0): 
                self.motors.turn(2000, constant_speed/2, constant_speed)
            else:
                self.motors.turn(2000, constant_speed, constant_speed/2)    


if __name__ == '__main__':
    arn = Arnold()
    arn.live()
