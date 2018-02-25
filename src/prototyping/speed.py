from motor import ArnoldMotors

robot = ArnoldMotors({'frontLeft':'outA','frontRight':'outB','rearLeft':'outC','rearRight':'outD'})
time = 5000
robot.move_forwards(time, 1050)
while (robot.isMoving()):
        print(robot.frontLeft.getSpeed())
