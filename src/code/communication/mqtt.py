#! /usr/bin/python3
import paho.mqtt.client as mqtt
from copy import deepcopy


class MqttHelper:
    def __init__(self):
        self.client = mqtt.Client()
        self.client.username_pw_set(username='gdsszota', password='F6am0LwBcGBG')
        self.messageQueue = []


    '''
        This method connects the client to the cloud mqtt helper. 
        It also sets the callback to the received_message function of the Helper.
    '''
    def connect(self):
        self.client.connect('m12.cloudmqtt.com', 19634, 60)
        self.client.subscribe('arnold/+')
        
        self.client.on_message = self.received_message

    '''
        We want the option of using the loop manually
        So we need to explicitly start listening/stop listening
        The loop also applies to sending stuff, so we need to call listen
        before sending stuff
    '''
    def listen(self):
        self.client.loop_start()


    '''
        Call this to sotp listening
    '''
    def stop_listening(self):
        self.client.loop_stop()

    '''
        This is called when a new message is received.
        Because we don't want to block the thread for long, we just add the payload to a message queue
    '''
    def received_message(self, client, userdata, message):
        self.messageQueue.append(message.payload.decode())
   
    '''
        Publish a message under the arnold/test topic
    '''
    def send_message(self, message):
        self.client.publish('arnold/test', message)

    '''
        Getter for the message queue. It's important that we don't change this
        as we need to clear the queue before returning it
    '''
    def getMQ(self):
        return_value = deepcopy(self.messageQueue)
        self.messageQueue.clear()

        return return_value


