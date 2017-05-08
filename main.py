#!/usr/bin/env python3
from time import sleep
from ev3dev.ev3 import *
from tree_list import *
sonarMotor  = MediumMotor(OUTPUT_D)
leftMotor  = LargeMotor(OUTPUT_B)
rightMotor = LargeMotor(OUTPUT_C)
# liftMotor  = LargeMotor(OUTPUT_D) #Unconnected

gs  = GyroSensor(INPUT_4);	assert gs.connected
cs  = ColorSensor(INPUT_3);	assert cs.connected
usR = UltrasonicSensor(INPUT_1);	assert usR.connected
usL = UltrasonicSensor(INPUT_2);	assert usL.connected
btn = Button()
cs.mode = 'COL-COLOR'

'''
some global vars and initialisation
'''
status=0
# cordinate of robot's postion
x = 0
y = 0
# face direction of robot
head_dir = 0
'''
store the last detecting distance at front
so it could be possible to calculation
'''
lastFrontDis=usL.value()*10

# initialisation the tree var
tree = Tree()

# to record the walls of its three side
branch_front = -1
branch_left  = -1
branch_right = -1
# theshold of detecting a wall
wall_distance= 100


def motor_move(leftSpeed=300,rightSpeed=300):
	leftMotor.run_forever(speed_sp=-leftSpeed)
	rightMotor.run_forever(speed_sp=-rightSpeed)

def motor_stop():
    leftMotor.stop()
    rightMotor.stop()
    motor_move(0,0)
def refresh_cor(distance):
    global x,y,head_dir
    # use head_dir to refresh the cordinate
    # distance /=420 # A3 size
    distance /=300 # test area size
    distance = int(round(distance,1))
    if   head_dir ==   0:
        x+= distance
    elif head_dir ==  90:
        y+= distance
    elif head_dir == 180:
        x-= distance
    elif head_dir == 270:
        y-= distance

def turn(to_dir, turning_speed = 250, reversing_speed = 30):
    global head_dir
    direction = 1
    angle = to_dir - head_dir
    if angle > 180:
        angle -= 180
        direction = -1
    if angle < 0 and angle > -180:
        angle += 180
        direction = -1
    if angle <= -180:
        angle += 360

    if angle == 0: return 0
    # print("angle:", angle)
    # print("direction", direction)
    gs.mode = 'GYRO-RATE'
    gs.mode = 'GYRO-ANG'

    # print("*",gs.value())
    #make a turn
    leftMotor.run_forever(speed_sp = direction * turning_speed *(-1))
    rightMotor.run_forever(speed_sp = - direction * turning_speed *(-1))

    while gs.value() * direction < angle:
        # print(gs.value())
        sleep(0.005)

    rightMotor.stop()
    leftMotor.stop()

    # print("*", gs.value())

    while gs.value() * direction > angle:
        leftMotor.run_forever(speed_sp = direction * reversing_speed)
        rightMotor.run_forever(speed_sp = - direction * reversing_speed)
        # print(gs.value())
        sleep(0.005)

    rightMotor.stop()
    leftMotor.stop()

    # print("*",gs.value())

    head_dir = to_dir
    return 1
#to_dir 0 - front, 90 - left
def us_turn(to_dir, turning_speed = 250):

    pos = [1,-89]
    if to_dir == 0:
        distance = pos[0]
    else:
        distance = pos[1]
    # print(distance)
    if distance == 0: return 0
    start = sonarMotor.position
    # print("start:", start)

    sonarMotor.run_to_abs_pos(position_sp = distance, speed_sp = turning_speed, stop_action = "brake")

    sleep(1)

    finish = sonarMotor.position
    # print("finish:",finish)

    us_dir = to_dir
    return 1
def found_new_node():
    global lastFrontDis, branch_right, branch_left, branch_front, wall_distance, head_dir

    # to get the walls around
    if usR.value()>wall_distance:
        branch_right =0
    else:
        branch_right = -1
    if usL.value()*10>wall_distance:
        branch_left =0
    else:
        branch_left = -1
    us_turn(0)
    # detecting the distance at front
    if usL.value()*10>wall_distance:
        branch_front =  0
    else:
        branch_front = -1

    # refresh the cordinate of this position
    print ('lastFrontDis ', lastFrontDis, 'usl value', usL.value())
    refresh_cor(lastFrontDis-usL.value()*10)
    # get all the walls info into the tree
    if tree.find_node(x,y)=='NULL':
        this_node= tree.add_node(x,y,branch_front,branch_left,branch_right,head_dir)
    else :
        this_node = tree.find_node(x,y)
    # turn to the new direction that computer decide
    head_dir=this_node.move_to(head_dir)
    turn(head_dir)
    # refresh this branch length to the end
    lastFrontDis = usL.value()

    # back to the side mode of right sonar
    us_turn(90)





print ('finished initialisation')
# while not btn.any():
#     sleep(0.1)




#start the main programme
while not btn.any() :

    print ("R dis:", usR.value(), "L dis:", usL.value()*10)
    if usR.value()>wall_distance or usL.value()*10>wall_distance:
        if status!=1:
            status=1
            # to move forward a bit to get the center of the branch
            sleep(0.5)
            motor_stop()
            found_new_node()
            # to get into the branch
            motor_move()
            sleep(1)

    elif cs.value()!=0 and cs.value()!=5 :
        # detected a wall
        if status!=2:
            status=2
            motor_stop()
            found_new_node()
            # to get into the branch
            motor_move()
            sleep(1)
    # elif cs.value() == 5:
    #     # found the can
    #     if status!=3:
    #         status=3
    #
    #         # set the information of this node
    #         found_new_node()
    #
    #         '''grap the can and go back'''
    #         # grap the can
    #         Sound.speak('found the can').wait()
    #
    #         # go back
    #         us_turn(0)
    #         while x!=0 or y!=0:
    #             branch_distance = usR.value()
    #
    #             while !(branch_distance< usR.value()):


    else:
        if status!=4:
            motor_move()
            status=4




# end programme
rightMotor.stop()
leftMotor.stop()
