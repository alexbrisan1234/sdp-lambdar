import ev3dev.ev3 as ev3

class Motor:

    def __init__(self, outPort):
        self.motor = ev3.LargeMotor(outPort)
        
    def run(self, duration, speed):
        self.motor.run_timed(time_sp = duration, speed_sp = speed)

    def set_polarity(self, polarity):
        if polarity == -1:
            self.motor.polarity = ev3.LargeMotor.POLARITY_INVERSED
        elif polarity == 1:
            self.motor.polarity = ev3.LargeMotor.POLARITY_NORMAL
        else:
            raise ValueError("Unknown value of polarity entered. Please use -1 or 1")
            
    def stop(self):
        self.motor.stop()
