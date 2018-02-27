#!/usr/bin/python3

import smbus

class I2C:
    '''Encapsulates the message sending protocol for Arnold'''
    def __init__(self, bus_num):
        'bus_num = port slave connected to + 2'
        # initate bus with bus number
        self.bus = smbus.SMBus(bus_num)


    def send_message(self, addr, msg):
        '''addr = i2c device bus address
           msg = a string of character to send
        '''
        # iterate over the string given and send it as an integer over
        # i2c bus
        [self.bus.write_byte(addr, ord(byte)) for byte in msg]

    def read_message(self, addr, terminator='Z'):
        ''' Will read from the slave at addr until it reads the terminator
               addr = i2c devic e bus address
               terminator = string that will stop the read loop
        '''
        # Convert byte received from the slave into a character
        msg = chr(self.bus.read_byte(addr))
        # Process message until a terminator character is recieved
        while msg[-1] != terminator:
            msg += chr(self.bus.read_byte(addr))

        return msg
