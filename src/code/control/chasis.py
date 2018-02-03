from axle import Axle




class Chasis:
    MODE_FWD = 0
    MODE_RWD = 1
    MODE_AWD = 2

    
    def __init__(self, frontLeft, frontRight, rearLeft, rearRight):
        self.frontAxle = Axle(frontLeft, frontRight, orientation=-1)
        self.rearAxle = Axle(rearLeft, rearRight)
        self.mode = Chasis.MODE_AWD

    def move_forward(self, duration, speed):
        if self.mode == Chasis.MODE_FWD:
            self.frontAxle.run_straight_line(duration, speed)
        elif self.mode == Chasis.MODE_RWD:
            self.rearAxle.run_straight_line(duration, speed)
        elif self.mode == Chasis.MODE_AWD:
            self.frontAxle.run_straight_line(duration, speed)
            self.rearAxle.run_straight_line(duration, speed)
        else:
            raise ValueError("Unknown value of traction mode")

    def move_backwards(self, duration, speed):
        if self.mode == Chasis.MODE_FWD:
            self.frontAxle.run_backwards_straight(duration, speed)
        elif self.mode == Chasis.MODE_RWD:
            self.rearAxle.run_backwards_straight(duration, speed)
        elif self.mode == Chasis.MODE_AWD:
            self.frontAxle.run_backwards_straight(duration, speed)
            self.rearAxle.run_backwards_straight(duration, speed)
        else:
            raise ValueError("Unknown value of traction mode")

    def move_left(self, duration, speed):
        if self.mode == Chasis.MODE_FWD:
            self.frontAxle.run_left(duration, speed)
            self.rearAxle.run_straight_line(duration, speed/10)
        elif self.mode == Chasis.MODE_RWD:
            self.rearAxle.run_left(duration, speed)
            self.frontAxle.run_straight_line(duration, speed/10)
        elif self.mode == Chasis.MODE_AWD:
            self.frontAxle.run_left(duration, speed)
            self.rearAxle.run_left(duration, speed)
        else:
            raise ValueError("Unknown value of traction mode")

    def move_right(self, duration, speed):
        if self.mode == Chasis.MODE_FWD:
            self.frontAxle.run_right(duration, speed)
            self.rearAxle.run_straight_line(duration, speed/10)
        elif self.mode == Chasis.MODE_RWD:
            self.rearAxle.run_right(duration, speed)
            self.frontAxle.run_straight_line(duration, speed/10)
        elif self.mode == Chasis.MODE_AWD:
            self.frontAxle.run_right(duration, speed)
            self.rearAxle.run_right(duration, speed)
        else:
            raise ValueError("Unknown value of traction mode")

    def change_mode(self, new_mode):
        if new_mode in [Chasis.MODE_FWD, Chasis.MODE_RWD, Chasis.MODE_AWD]:
            self.mode = new_mode
        else:
            raise ValueError("Trying to set to invalid mode")
