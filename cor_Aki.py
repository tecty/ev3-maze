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
<!-- abandoned -->
store the last detecting distance at front
so it could be possible to calculation
# lastFrontDis=usL.value()
'''

# store the distance to the wall before cor_move
before_distance=0
# store whether the sensor detected red color
is_color=0
# initialisation the tree var
tree = Tree()

"""
<!-- abandoned -->
# to record the walls of its three side
branch_front = -1
branch_left  = -1
branch_right = -1
"""

"""config part"""
# length of one unit
unit_length=300
# theshold of detecting a wall
wall_distance= unit_length*2/3
# the color of the can 5 is red
can_color =5


def motor_move(leftSpeed=250,rightSpeed=250):
	leftMotor.run_forever(speed_sp=-leftSpeed)
	rightMotor.run_forever(speed_sp=-rightSpeed)

def motor_stop():
    leftMotor.stop()
    rightMotor.stop()
    motor_move(0,0)
def refresh_cor(head_dir):
    """new method to refresh_cor"""
    global x,y
    if head_dir == 0:
        y+=1
    elif head_dir==90:
        x+=1
    elif head_dir==180:
        y-=1
    elif head_dir==270:
        x-=1
    """
    <!-- abandoned method -->
    global x,y,head_dir
    # use head_dir to refresh the cordinate
    # distance /=420 # A3 size
    # distance /=300 # test area size
    # distance = int(round(distance,1))
    if  head_dir  ==   0:
        x+= distance
    elif head_dir ==  90:
        y+= distance
    elif head_dir == 180:
        x-= distance
    elif head_dir == 270:
        y-= distance
    """


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

    sleep(1.5)

    finish = sonarMotor.position
    # print("finish:",finish)

    us_dir = to_dir
    return 1

def is_wall(dir):
    # return -1 has wall return 0 have a branch
    if   dir == 'l':
        us_turn(90)
        dis = usL.value()
    elif dir == 'f':
        us_turn(0)
        dis = usL.value()
    elif dir == 'r':
        dis = usR.value()*10

    if dis < wall_distance:
        # there is a wall in that direction
        return -1
    return 0

"""
<!-- abandoned method -->
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
    refresh_cor(lastFrontDis-(usL.value()*10))
    # get all the walls info into the tree
    if tree.find_node(x,y)=='NULL':
        this_node= tree.add_node(x,y,branch_front,branch_left,branch_right,head_dir)
    else :
        this_node = tree.find_node(x,y)
    # turn to the new direction that computer decide
    turn(this_node.move_to(head_dir))
    # refresh this branch length to the end
    lastFrontDis = usL.value()*10

    # back to the side mode of right sonar
    us_turn(90)

print("finished initialisation")
# inital the first node
if lastFrontDis > wall_distance:
    branch_front = 0
else:
    branch_front = -1
us_turn(90)
if usR.value()>wall_distance:
    branch_right = 0
else :
    branch_right = -1
if usL.value()>wall_distance:
    branch_left = 0
else :
    branch_left = -1
# get all the walls info into the tree
if tree.find_node(x,y)=='NULL':
    this_node= tree.add_node(x,y,branch_front,branch_left,branch_right,head_dir)
else :
    this_node = tree.find_node(x,y)
# turn to the new direction that computer decide
head_dir=this_node.move_to(head_dir)
turn(head_dir)
print("initialized first node")
"""





# test is_wall
# print("left has",is_wall('l'))
# print("right has",is_wall('r'))
# print("front has",is_wall('f'))


# test cor_move
def cor_move(head_dir):
    global before_distance, is_color
    # refresh the global cordinate by its head direction
    refresh_cor(head_dir)
    us_turn(0)
    # record the position before it move forward
    before_distance = rightMotor.position
    to_distance = usL.value()-unit_length
    print("to_distance = ",to_distance,"unit_length=",unit_length,"usvalue",usL.value())
    if to_distance < 50:
        to_distance = 50
        print("to_distance = ",to_distance)
    motor_move()
    while usL.value()>to_distance and (not btn.any()) and is_color==0:
        sleep(0.01)
        if cs.value()== can_color:
            motor_stop()
            sleep(0.01)
            if cs.value()== can_color:
                is_color=1
            else:
                motor_move()
        else:
            motor_move()
    motor_stop()




if __name__ == '__main__':
    print("finished initialisation")
    while (not btn.any()) and  is_color== 0:
        """ordinary movement by cor"""
        if tree.find_node(x,y)=='NULL':
            this_node= tree.add_node(x,y,is_wall('f'),is_wall('l'),is_wall('r'),head_dir)
        else :
            this_node = tree.find_node(x,y)
        this_node.print_node()
        to_dir =this_node.move_to(head_dir)
        turn(to_dir)
        cor_move(head_dir)

    """code after found the can"""

    print("find the red can")
    # sound the alarm of found the can
    Sound.tone([(1000, 500, 500)] * 3)
    # set the node for the can at.
    if tree.find_node(x,y)=='NULL':
        this_node= tree.add_node(x,y,-1,-1,-1,head_dir)
    else :
        this_node = tree.find_node(x,y)
    this_node.print_node()

    # revise to the last node
    motor_move(-200,-200)
    print("old position is",rightMotor.position,"before_distance is",before_distance)
    while (not btn.any()) and rightMotor.position<before_distance:
        sleep(0.01)
    motor_stop()

    # now is at the node before
    to_dir = this_node.move(head_dir)
    #turn 180 degree
    turn(to_dir)
    #refresh the cordinate by a low level func so it won't move
    refresh_cor(head_dir)

    # revise its route
    print("now is retreat it's route")
    while (x!=0 or y!=0) and not btn.any() :
        this_node = tree.find_node(x,y)
        this_node.print_node()
        to_dir =this_node.back_to(head_dir)
        turn(to_dir)
        cor_move(head_dir)
        print ("next dir is",head_dir)

    print("finally here is:",x,",",y)

    motor_stop()
    print("end of the programme")
