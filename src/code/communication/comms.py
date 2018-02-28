#! /usr/bin/python3
import serial
import time


class Serial_Comm:
    def __init__(self, oport="/dev/ttyACM0", obaudrate=9600, otimeout=None):
        self.ser = serial.Serial(port=oport, baudrate=obaudrate, timeout=otimeout)

        # Set the signal codes, identify the beginning and end of a signal
        self.no_sig = 4294967295

    def read_message(self):
        '''
            Read a line at a time from the input buffer while it's not empty.
        '''
        self.initiate_transmission()

        # Message is essentially a list with some checking functions
        msgs = (None, None)
        while self.ser.inWaiting() > 0:
            msg = Message()
            while not msg.is_closed():
                try:

                    # Receive the message as a string
                    sm = self.ser.readline().strip()
                    # Convert to integer opcode
                    opcode = int(sm)
                    self.ser.flush();

                    msg.append(opcode)

                    if msg.is_well_formed():
                        if msg.msg_type == 'ultrasonic':
                            msgs = (msg, msgs[1])
                        elif msg.msg_type == 'infrared':
                            msgs = (msgs[0], msg)
                        break

                except ValueError:
                    continue
                except KeyboardInterrupt:
                    print('Aborting Robot Operation')
                    exit()
        return msgs

    def send_to_serial(self, message):
        self.initiate_transmission()
        return self.ser.write(message.encode('utf-8'))

    def initiate_transmission(self):
        '''Open the port to request data'''
        if not self.ser.isOpen():
                self.ser.open()

    def terminate_transmission(self):  
        '''Close the port'''
        if self.ser.isOpen():
            self.ser.close()

class Message(list):
    # Give the type of the message
    msg_type = None

    open_message = 0xFFFFFFFE
    close_message = 0xFFFFFFFD


    ids = {'ultrasonic':0xFFFFFFFC,'infrared':0xFFFFFFFB}
    no_sig = 0xFFFFFFFF
    timestamp = 0

    def is_well_formed(self):
        'Checks if the message is fit to pass to planning'
        if len(self) < 3: return False

        wf = True
        if not self[0] == self.open_message: wf = False
        if not self[-1] == self.close_message: wf = False
        if self.get_left() == self.no_sig or self.get_right() == self.no_sig: wf = False

        if not self[1] in self.ids: wf = False

        return wf


    def append(self, item):
        ''' 
            Extension of list append assigns a type to the class
        '''
        if not self.is_open() and item != self.open_message:
            return

        if len(self) == 0:
            self.timestamp = int(round(time.time() * 1000))

        if len(self) > 2:
            if self[1] == self.ids['ultrasonic']:
                self.msg_type = 'ultrasonic'
            if self[1] == self.ids['infrared']:
                self.msg_type = 'infrared'

        super(Message, self).append(item)

    def is_open(self):
        try:
            if self[0] == self.open_message and self[-1] != self.close_message:
                return True
        except IndexError:
            pass

        return False

    def is_closed(self):
        try:
            if self[-1] == self.close_message:
                return True
        except IndexError:
            pass

        return False

    def get_infrared_sensor_data(self, sensor_no):
        if self.msg_type != 'infrared':
            raise ValueError

        return self[sensor_no+2]

    def get_left(self):
        if self.msg_type != 'ultrasonic':
            raise ValueError

        return self[2]

    def get_right(self):
        if self.msg_type != 'ultrasonic':
            raise ValueError

        return self[3]

if __name__ == '__main__':
    ard = Serial_Comm()

    while True:
        msgs = ard.read_from_serial()
        print('Ultrasonic: ', msg[0])
        print('Infrared: ', msg[1])

