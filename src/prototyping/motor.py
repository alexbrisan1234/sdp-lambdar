import ev3dev.ev3 as ev3

class Motor:

    def __init__(self, outPort):
        self.motor = ev3.LargeMotor(outPort)
        
    def run(self, duration, speed):
        self.motor.run_timed(time_sp = duration, speed_sp = speed)
            
    def stop(self):
        self.motor.stop()

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
