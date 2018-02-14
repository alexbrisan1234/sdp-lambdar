import ev3dev.ev3 as ev3
from functools import reduce
from math import pi

class Motor:

    def __init__(self, outPort):
        self.motor = ev3.LargeMotor(outPort)
        
    def run(self, duration, speed):
        self.motor.run_timed(time_sp = duration, speed_sp = speed)
            
    def stop(self):
        self.motor.stop()
        
    ''' 
    measures the speed according to revs / sec of the motor
    NOTICE: even if there's something blocking the robot
    the wheel keeps turning and hence the measurement is inaccurate
    ''' 
    def getSpeed(self):
        wheelDiameter = 8.2 #cm
        wheelCircumference = 2*pi*wheelDiameter/2 #cm
        speedSum = 0
        count = 0
        while (self.motor.is_running and count < 10):
            # revs / sec = (degrees / sec) / ((degrees / rotation)=360)
            bigGearRps = (self.motor.speed / self.motor.count_per_rot)
            # big gear has 40 teeth, small has 24
            rps = bigGearRps * 40 / 24
            #instantaneous speed
            speedSum = speedSum + wheelCircumference * rps
            count = count + 1
        if (count == 0):
            return 0
        return round(speedSum/count)
        
class ArnoldMotors:
    def __init__(self, portDict):
        self . frontLeft = Motor(portDict['frontLeft'])
        self . frontRight = Motor(portDict['frontRight'])
        self . rearLeft = Motor(portDict['rearLeft'])
        self . rearRight = Motor(portDict['rearRight'])

        self . left = [self.frontLeft, self.rearLeft]
        self . right = [self.frontRight, self.rearRight]

        self . motors = self . left + self . right
        
    def turn(self, duration, speedLeft, speedRight):
        # Run the left side
        for leftMotor in self . left:
            leftMotor . run(duration, speedLeft)

        # Run the right side
        for rightMotor in self . right:
            rightMotor . run(duration, speedRight)

    def move_forwards(self, duration, speed):
        for arnoldMotor in self.motors:
            arnoldMotor . run(duration, speed)

    def move_backwards(self, duration, speed):
        for arnoldMotor in self.motors:
            # Multiply speed by -1 to achieve backwards motion
            arnoldMotor.run(duration, -1 * speed)
            
    def isMoving(self):
        #return reduce((lambda m1, m2: m1.motor.is_running or m2.motor.is_running), self.motors)
        return any([m.motor.is_running for m in self.motors])
    def stop(self):
       for motor in self.motors:
           motor.stop()
