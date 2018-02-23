import ev3dev.ev3 as ev3
from math import pi

class Motor:

    def __init__(self, outPort, polarity = 1):
        self.motor = ev3.LargeMotor(outPort)
        if (polarity == -1):
            self.motor.polarity = 'inversed'
        else:
            self.motor.polarity = 'normal'
        
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
        # revs / sec = (degrees / sec) / ((degrees / rotation)=360)
        bigGearRps = (self.motor.speed / self.motor.count_per_rot)
        # big gear has 40 teeth, small has 24
        rps = bigGearRps * 40 / 24
        #instantaneous speed
        speed = wheelCircumference * rps
        return abs(round(speed))
        
class ArnoldMotors:
    def __init__(self, portDict):
        #front motors are facing opposite the rears
        self . frontLeft = Motor(portDict['frontLeft'], -1)
        self . frontRight = Motor(portDict['frontRight'], -1)
        self . rearLeft = Motor(portDict['rearLeft'])
        self . rearRight = Motor(portDict['rearRight'])
        self . left = [self.frontLeft, self.rearLeft]
        self . right = [self.frontRight, self.rearRight]
        self . motors = self.left + self.right
        
    def turn(self, duration, speedLeft, speedRight):
        # Run the left side
        for leftMotor in self . left:
            leftMotor . run(duration, speedLeft)

        # Run the right side
        for rightMotor in self . right:
            rightMotor . run(duration, speedRight)

    def move_forwards(self, duration, speed):
        for motor in self . motors:
            motor . run(duration, speed)

    def move_backwards(self, duration, speed):
        self.move_forwards(duration, -speed)
            
    def isMoving(self):
        return any([m.motor.is_running for m in self.motors])

    def stop(self):
       for motor in self.motors:
           motor.stop()
