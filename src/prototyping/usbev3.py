#! /usr/bin/python3
import serial
import time

ser = serial.Serial(port="/dev/ttyACM0", baudrate=9600, timeout=None)

def read_from_serial():
    '''
    Read a line at a time from the input buffer while it's not empty.
    '''
    initiate_transmission()
    message = ''
    while ser.inWaiting() > 0:
        message+= ser.readline().decode('ascii', 'ignore')
        print(message)
    return message

def send_to_serial(message):
    initiate_transmission()
    return ser.write(message.encode('utf-8'))

def initiate_transmission():
    '''Open the port to request data'''
    if(not(ser.isOpen())):
        ser.open()

def terminate_transmission():
    '''Close the port '''
    if(ser.isOpen()):
        ser.close()
