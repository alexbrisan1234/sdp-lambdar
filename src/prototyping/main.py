from comms import Serial_Comm
from enum import Enum

class Arnold:
    # Arnold's to main sensory inputs
    self.ultra_data
    self.infra_data

    class Mode(Enum):
        FOLLOW = 1
        OBSTACLE = 2

    self.acting_mode = Mode.FOLLOW

    def __init__(self):
        self.ser = Serial_Comm()


    def live(self):
        'Main loop of Arnold. Updates model and perform motions'
        while True:
            next_message = self.ser.read_message()

            if next_message.msg_type == 'ultrasonic':
                self.ultra_data = next_message
            else:
                self.infra_data = next_message

            # If the data from the ultrasonics is old then switch modes
            if int(round(time.time() * 1000)) - self.ultra_data.timestamp > 1000:
                self.acting_mode = Mode.OBSTACLE
            self.actuate()


    def actuate(self):
        if self.acting_mode = Mode.FOLLOW:
            pass
        else:
            pass
