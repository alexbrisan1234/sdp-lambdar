import ev3dev.ev3 as ev3

class Motor:

    def __init__(self, outPort):
        self.motor = ev3.LargeMotor(outPort)
        
    def run(self, duration, speed):
        self.motor.run_timed(time_sp = duration, speed_sp = speed)
        
    def stop(self):
        self.motor.stop()