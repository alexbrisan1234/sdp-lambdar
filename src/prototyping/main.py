from comms import Serial_Comm
from enum import Enum
from motor import *

class Arnold:
    # Arnold's to main sensory inputs
    self.ultra_data
    self.infra_data

    class Mode(Enum):
        FOLLOW = 1
        OBSTACLE = 2

    def __init__(self):
        self.motors = ArnoldMotor({'frontLeft':'A','frontRight':'B','rearLeft':'C','rearRight':'D'});
        self.acting_mode = Mode.FOLLOW

        self.ser = Serial_Comm()


    def live(self):
        'Main loop of Arnold. Updates model and perform motions'
        while True:
            try:
                next_message = self.ser.read_message()

                # Seperate data into ultrasonic and infrared
                if next_message.msg_type == 'ultrasonic':
                    self.ultra_data = next_message
                elif next_message.msg_type == 'infrared':
                    self.infra_data = next_message

                # If the data from the ultrasonics is old then switch modes
                if int(round(time.time() * 1000)) - self.ultra_data.timestamp > 1000:
                    self.acting_mode = Mode.OBSTACLE
                else:
                    self.acting_mode = Mode.FOLLOW

                # Update motion based on current
                self.actuate()
            except KeyboardInterrupt:
                break


    def actuate(self):
        'Logic for selecting an acutation strategy and activating motors'
        if self.acting_mode = Mode.FOLLOW:
            pass
        else:
            pass
