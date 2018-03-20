import ev3dev.ev3 as ev3
from math import pi

class Motor:

    def __init__(self, outPort, polarity = 1):
        self.motor = ev3.LargeMotor(outPort)
        if (polarity == -1):
            self.motor.polarity = 'inversed'
        else:
            self.motor.polarity = 'normal'

    #speed is a value from -1050 to 1050
    def run(self, speed):
        self.motor.run_forever(speed_sp = speed)

    #action belongs {brake, coast, hold}
    def stop(self, action='brake'):
        self.motor.stop(stop_action=action)

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

def sign(x):
    return -1 if x < 0 else 1

class ArnoldMotors:
    def __init__(self, portDict, speed=0, tr=0):
        #front motors are facing opposite the rears
        self . frontLeft = Motor(portDict['frontLeft'], -1)
        self . frontRight = Motor(portDict['frontRight'], -1)
        self . rearLeft = Motor(portDict['rearLeft'])
        self . rearRight = Motor(portDict['rearRight'])
        self . left = [self.frontLeft, self.rearLeft]
        self . right = [self.frontRight, self.rearRight]
        self . motors = self.left + self.right
        self.speed = speed
        self.tr = tr
        self.maxSpeed = 1000

    def move(self):
        speeds = self.calculateSpeeds()
        speedLeft = speeds[0]
        speedRight = speeds[1]
        # Run the left side
        for leftMotor in self . left:
            leftMotor . run(speedLeft)
        # Run the right side
        for rightMotor in self . right:
            rightMotor . run(speedRight)

    def calculateSpeeds(self):
        self.tr = min(1, max(-1, self.tr))
        assert abs(self.tr) <= 1 , str(self.tr)
        self.speed = min(self.speed, self.maxSpeed)
        #turning rate is a factor of the separately given speed
        speedLeft = self.speed * (1-abs(self.tr+1/2))
        speedRight = self.speed * (1-abs(self.tr-1/2))
        # assert round(abs(speedLeft) + abs(speedRight)) == round(self.speed), str(speedLeft) + " "+ str(speedRight) + " != " + str (self.speed)
        #adjusts for over / underflows
        speedRight = min(self.maxSpeed, max(-self.maxSpeed, speedRight))
        speedLeft = min(self.maxSpeed, max(-self.maxSpeed, speedLeft))
        return (speedLeft, speedRight)

    #turning rate should be between [-1,1]
    #-1 represents turn on the spot to the right
    #-0.5 turn to the right with one side no speed and the other full speed
    #0 goes straight
    def set_parameters(self, speed, tr):
        self.speed = speed
        self.tr = tr
        self.move()

    def set_speed(self, speed):
        self.set_parameters(speed, self.tr)

    def set_turning_rate(self, tr):
        self.set_parameters(self.speed, tr)

    def move_forwards(self, speed):
        self.set_parameters(speed, 0)

    def move_backwards(self, speed):
        self.move_forwards(-speed)

    def isMoving(self):
        return any([m.motor.is_running for m in self.motors])

    def stop(self, action = 'brake'):
       for motor in self.motors:
           motor.stop(action)
