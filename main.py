#!/usr/bin/env python3
from time import sleep
from ev3dev.ev3 import *
from tree_list import *
sonarMotor  = MediumMotor(OUTPUT_A)
leftMotor  = LargeMotor(OUTPUT_B)
rightMotor = LargeMotor(OUTPUT_C)
liftMotor  = LargeMotor(OUTPUT_D) #Unconnected

gs = TouchSensor(INPUT_4);	assert gs.connected #bug
cs = ColorSensor(INPUT_3);	assert cs.connected
usR  = UltrasonicSensor(INPUT_1);	assert usR.connected
usL  = UltrasonicSensor(INPUT_2);	assert usL.connected
btn = Button()
cs.mode = 'COL-COLOR'

 """ some global vars and initialisation """
status=0
# cordinate of robot's postion
x = 0
y = 0
# face direction of robot
head_dir = 0
"""
store the last detecting distance at front
so it could be possible to calculation
"""
lastFrontDis= 0


tree = Tree()

# to record the walls of its three side
branch_front = -1
branch_left  = -1
branch_right = -1



def motor_move(leftSpeed=300,rightSpeed=300):
	leftMotor.run_forever(speed_sp=-leftSpeed)
	rightMotor.run_forever(speed_sp=-rightSpeed)

def motor_stop():
    leftMotor.stop()
    rightMotor.stop()
    motor_move(0,0)
def refresh_cor(distance):
    # use head_dir to refresh the cordinate
    if   head_dir ==   0:
        x+= distance
    elif head_dir ==  90:
        y+= distance
    elif head_dir == 180:
        x-= distance
    elif head_dir == 270:
        y-= distance


lastFrontDis=usR.value()


print ('finished initialisation')
while not btn.any():
    sleep(0.1)
#start the main programme

while not btn.any():
    if usR.value()>100 or usL.value()>100:
        # found a branch
        if status!=1:
            status=1
            # to move forward a bit to get the center of the branch
            sleep(0.5)
            motor_stop()
            # to get the walls around
            if usR.value()>100:
                branch_right =0
            else:
                branch_right = -1
            if usL.value()>100:
                branch_left =0
            else:
                branch_left = -1
            us_turn(0)
            # detecting the distance at front
            if usR.value()>100:
                branch_front =  0
            else:
                branch_front = -1
            # refresh the cordinate of this position
            refresh_cor(lastFrontDis-usR.value())
            # get all the walls info into the tree
            if tree.find_node(x,y)=='NULL':
                this_node= tree.add_node(x,y,branch_front,branch_left,branch_right,head_dir)
            else :
                this_node = tree.find_node(x,y)
            # turn to the new direction that computer decide
            turn(this_node.move_to(head_dir))
            # refresh this branch length to the end
            lastFrontDis = usR.value

            # back to the side mode of right sonar
            us_turn(90)
            # to get into the branch
            motor_move()
            sleep(1)

    elif us.value()<500:
        if status!=2:
            status=2
            motor_move(1000,1000)
            if us.value()>400:
                motor_move(-600,600)
                sleep(1)
            motor_move(1000,1000)
    elif cs.value() == 1:
        if status!=3:
            status=3
            motor_move(-1000,-1000)
            sleep(0.6)
    else:
        if status!=4:
            motor_move(400,-400)
            status=4
rightMotor.stop()
leftMotor.stop()
