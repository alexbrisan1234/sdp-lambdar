#! /usr/bin/python3
import serial
import time


class Serial_Comm:
    def __init__(self):
        self.ser = serial.Serial(port="/dev/ttyACM0", baudrate=115200, timeout=None)

    def read_from_serial(self):
        '''
        Read a line at a time from the input buffer while it's not empty.
        '''
        self.initiate_transmission()
        while True:
            # print(int.from_bytes(self.ser.read(), 'big'))
            try:
                print(int(self.ser.readline().strip()))
                self.ser.flush();
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


if __name__ == '__main__':
    ard = Serial_Comm()

    ard.read_from_serial()

