from motor import Motor

class Axle:
    def __init__(self, leftPort, rightPort, orientation=1):
        # Connect the motors
        self.leftMotor = Motor(leftPort)
        self.rightMotor = Motor(rightPort)

        # Set initial polarity to take into account the orientation
        # of the motors
        self.leftMotor.set_polarity(orientation)
        self.rightMotor.set_polarity(orientation)

        # Save the orientation
        self.orientation = orientation
        
    def run_straight_line(self, duration, speed):
        self.leftMotor.run(duration, speed)
        self.rightMotor.run(duration, speed)

    def run_backwards_straight(self, duration, speed):
        # Switch polarity so we go backwards
        self.leftMotor.set_polarity(-1 * self.orientation)
        self.rightMotor.set_polarity(-1 * self.orientation)

        # Execute the motion
        self . leftMotor . run(duration, speed)
        self . rightMotor . run(duration, speed)

        # Set polairty back to normal
        self.leftMotor.set_polarity(1 * self.orientation)
        self.rightMotor.set_polarity(1 * self.orientation)

    def __run_corner_straight(self, motorA, motorB, duration, speed):
        motorA.set_polarity(-1 * self.orientation)
        motorB.set_polarity(1 * self.orientation)

        motorA.run(duration, speed / 2)
        motorB.run(duration, speed)

        motorA.set_polarity(1 * self.orientation)
        
    def run_left(self, duration, speed):
        self.__run_corner_straight(
            self.leftMotor,
            self.rightMotor,
            duration,
            speed
        )

    def run_right(self, duration, speed):
        self.__run_corner_straight(
            self.rightMotor,
            self.leftMotor,
            duration,
            speed
        )
