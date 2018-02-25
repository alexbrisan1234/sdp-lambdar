from comms import Serial_Comm
from enum import Enum
from motor import *
import time

class Arnold:
    # Arnold's to main sensory inputs
    ultra_data = None
    infra_data = None

    class Mode(Enum):
        FOLLOW = 1
        OBSTACLE = 2

    def __init__(self):
        self.motors = ArnoldMotors({'frontLeft':'A','frontRight':'B','rearLeft':'C','rearRight':'D'});
        self.acting_mode = self.Mode.FOLLOW

        self.ser = Serial_Comm()


    def live(self):
        'Main loop of Arnold. Updates model and perform motions'
        while True:
            try:
                print('Getting Message')
                new_data = self.ser.read_message()

                if new_data[0] != None:
                    self.ultra_data = new_data[0]

                if new_data[1] != None:
                    self.infra_data = new_data[1]

                print(self.ultra_data)
                
                # If the data from the ultrasonics is old then switch modes
                if self.ultra_data != None and int(round(time.time() * 1000)) - self.ultra_data.timestamp > 1000:
                    self.acting_mode = self.Mode.OBSTACLE
                else:
                    self.acting_mode = self.Mode.FOLLOW

                # Update motion based on current
                self.actuate()
            except KeyboardInterrupt:
                print('Aborting Robot Operation')
                break


    def actuate(self):
        'Logic for selecting an acutation strategy and activating motors'
        print('Actuating')
        if self.acting_mode == self.Mode.FOLLOW:
            pass
        else:
            pass


if __name__ == '__main__':
    arn = Arnold()
    arn.live()
