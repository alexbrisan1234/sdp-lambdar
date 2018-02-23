#! /usr/bin/python3
import serial
import time


class Serial_Comm:
    def __init__(self, oport="/dev/ttyACM0", obaudrate=115200, otimeout=None):
        self.ser = serial.Serial(port=oport, baudrate=obaudrate, timeout=otimeout)

        # Set the signal codes, identify the beginning and end of a signal
        self.no_sig = 4294967295

        self.open_message = 4294967294
        self.close_message = 4294967293

    def read_message(self):
        '''
            Read a line at a time from the input buffer while it's not empty.
        '''
        self.initiate_transmission()

        # Message is essentially a list with some checking functions
        msg = Message()
        message_is_open = False
        message_is_ended = False
        while not message_is_ended:
            try:
                opcode = int(self.ser.readline().strip())
                self.ser.flush();

                if opcode == self.open_message:
                    msg = []
                    self.message_is_open = True

                if message_is_open:
                    msg.append(opcode)

                    # Ensures the message is being formed correctly
                    if msg.is_well_formed():
                        return msg

            except ValueError:
                continue
            except KeyboardInterrupt:
                exit()
        return '' 

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

    ids = [4294967292,4294967291]
    timestamp = 0

    def is_well_formed(self):
        'Checks if the message is fit to pass to planning'
        wf = True
        if not self[0] == 4294967294: wf = False
        if not self[-1] == 4294967295: wf = False

        if not self[1] in self.ids: wf = False

        return wf


    def append(self, item):
        ''' 
            Extension of list append assigns a type to the class
        '''
        if len(self) == 0:
            self.timestamp = int(round(time.time() * 1000))

        if len(self) > 2:
            if self[1] == self.ids[0]:
                self.msg_type = 'ultrasonic'
            if self[1] == self.ids[1]:
                self.msg_type = 'infrared'

        super(Message, list).append(item)


if __name__ == '__main__':
    ard = Serial_Comm()

    ard.read_from_serial()

