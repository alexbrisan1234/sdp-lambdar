from motor import Motor

motorLeftFront = Motor('outB')
motorLeftRear = Motor('outC')
motorRightFront = Motor('outA')
motorRightRear = Motor('outD')

'''
Turns robot according to the speed parameters.
if speedRight > speedLeft => turn left.
if speedRight < speedLeft => turn right.
'''
def move(duration, speedRight, speedLeft):
    motorLeftFront.run(duration, speedLeft)
    motorLeftRear.run(duration, -speedLeft)
    motorRightFront.run(duration, speedRight)
    motorRightRear.run(duration, -speedRight)
    
def turn(duration, speedRight, speedLeft):
    move(duration, speedRight, speedLeft)

def move_forwards(duration, speed):
    move(duration, speed, speed)

def move_backwards(duration, speed):
    move(duration, -1 * speed, -1 * speed)

#def main():
    #move_forwards(3000, 60)
    #turn(5000, 10, 50)
    #move_forwards(3000, 60)
    
#main()