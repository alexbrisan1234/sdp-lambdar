#! /usr/bin/python3
import serial
import time
import re
from .leds import light_left, light_right
import os

__DEBUG__ = False

ultra_pattern = re.compile('^<U([0-9]{1,10}|-) ([0-9]{1,10}|-)>$')
infra_pattern = re.compile('^<I([0-9]{1,10}|-) ([0-9]{1,10}|-) ([0-9]{1,10}|-)>$')
lock_pattern = re.compile('^<[CO]>$')

class Serial_Comm:
    def __init__(self, oport=None, obaudrate=115200, otimeout=None):
        if oport == None:
            ports = os.listdir('/dev/')
            oport = '/dev/'+[p for p in ports if 'ACM' in p][0]

        self.ser = serial.Serial(port=oport, baudrate=obaudrate, timeout=otimeout)
        self.ser.read(self.ser.inWaiting())

        # Set the signal codes, identify the beginning and end of a signal
        self.no_sig = 0xFFFFFFFF

        self.partial_msg = ''

    def clear_buffer(self):
        self.ser.read(self.ser.inWaiting())

    def read_message(self):
        '''
            Read a line at a time from the input buffer while it's not empty.
        '''
        self.initiate_transmission()

        # Message is essentially a list with some checking functions
        msgs = (None, None, None)
        inBuffer = self.ser.inWaiting()
        if __DEBUG__: print(self.ser.inWaiting())
        try:
            # Read the entire buffer string and convert to list of strings
            buf = self.partial_msg + self.ser.read(inBuffer).decode(errors='ignore')
            lines = buf.split('|')
            if __DEBUG__: print(lines)  # VERY useful
            if ultra_pattern.match(lines[-1]) or infra_pattern.match(lines[-1]) or lock_pattern.match(lines[-1]):
                self.partial_msg = ''
            else:
                self.partial_msg = lines[-1]

            ultraRead = None
            infraRead = None
            lockRead = None
            for line in reversed(lines):
                if ultraRead == None and ultra_pattern.match(line): ultraRead = self.messagize(line)
                elif infraRead == None and infra_pattern.match(line): infraRead = self.messagize(line)
                #if we send on change, we need to iterate through all the list
                elif lockRead == None and lock_pattern.match(line): lockRead = self.messagize(line)
            
            msgs = (ultraRead, infraRead, lockRead)

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

    def messagize(self, element):
        try:
            return Message(element)
        except IOError:
            return ''

class Message(list):
    # Give the type of the message
    msg_type = None
    no_sig = 0xFFFFFFFF
    timestamp = 0

    def __init__(self, msg):
        #STM Filtering data more

        if lock_pattern.match(msg):
            self.msg_type = 'lock'
            if msg == '<C>':
                if __DEBUG__: print('Lock message received: ', msg)
                self.append('close')
            elif msg == '<O>':
                if __DEBUG__: print('Lock message received: ', msg)
                self.append('open')
            return

        values = [int(d) if d != '-' else self.no_sig for d in msg[2:-1].split(' ')]
        self.timestamp = int(round(time.time() * 1000))

        if ultra_pattern.match(msg):
            self.msg_type = 'ultrasonic'
            if __DEBUG__: print('Ultra message received: ', msg)
            if self.no_sig in values:
                if (values[0]==self.no_sig):
                    light_right(0)
                if (values[1]==self.no_sig):
                    light_left(0)
                raise IOError('Signal not received on one/both ultrasonic sensors')
            else:
                light_left(1)
                light_right(1)
        elif infra_pattern.match(msg):
            if __DEBUG__: print('Infra message received: ', msg)
            self.msg_type = 'infrared'
        else: 
            raise IOError('Message was not well formed')

        for d in values:
            self.append(d)


    def get_infrared_sensor_data(self, sensor_no):
        if self.msg_type != 'infrared':
            raise ValueError(self.msg_type)

        return self[sensor_no]

    def get_left(self):
        if self.msg_type != 'ultrasonic':
            raise ValueError(self.msg_type)

        return self[0]

    def get_right(self):
        if self.msg_type != 'ultrasonic':
            raise ValueError

        return self[1]

if __name__ == '__main__':
    ard = Serial_Comm()

    while True:
        msgs = ard.read_message()
        if __DEBUG__: print('Ultrasonic: ', msg[0])
        if __DEBUG__: print('Infrared: ', msg[1])

