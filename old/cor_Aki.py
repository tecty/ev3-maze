#!/usr/bin/python3
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

# store the distance to the wall before cor_move
before_distance=0
# store whether the sensor detected red color
is_color=0
# initialisation the tree var
tree = Tree()

"""config part these values should be modify """
# length of one unit
unit_length=830
# theshold of detecting a wall
wall_distance= 280
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
    gs.mode = 'GYRO-RATE'
    gs.mode = 'GYRO-ANG'

    #make a turn
    leftMotor.run_forever(speed_sp = direction * turning_speed *(-1))
    rightMotor.run_forever(speed_sp = - direction * turning_speed *(-1))

    while gs.value() * direction < angle:
        sleep(0.005)

    motor_stop()
    sleep(0.1)

    while gs.value() * direction > angle:
        leftMotor.run_forever(speed_sp = direction * reversing_speed)
        rightMotor.run_forever(speed_sp = - direction * reversing_speed)
        sleep(0.005)

    motor_stop()
    sleep(0.1)

    head_dir = to_dir
    return 1
#to_dir 0 - front, 90 - left
def us_turn(to_dir, turning_speed = 250):

    pos = [1,-89]
    if to_dir == 0:
        distance = pos[0]
    else:
        distance = pos[1]
    if distance == 0: return 0
    start = sonarMotor.position

    sonarMotor.run_to_abs_pos(position_sp = distance, speed_sp = turning_speed, stop_action = "brake")

    sleep(1.5)

    finish = sonarMotor.position

    us_dir = to_dir
    return 1

def is_wall(dir):
    # return -1 has wall return 0 have a branch
    if dir == 'l' or dir == 'r':
        us_turn(90)
        # us the sum of the sensor to detect the walls on the both side
        # 1000 should be modify
        if usL.value()+usR.value()*10<340:
            return -1
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

# test cor_move
def cor_move(head_dir,modfiyable=0):
    global before_distance, is_color
    # refresh the global cordinate by its head direction
    refresh_cor(head_dir)
    us_turn(0)
    # record the position before it move forward
    before_distance = rightMotor.position
    to_distance = rightMotor.position-unit_length
    print("to_distance = ",to_distance,"unit_length=",unit_length,"usvalue",usL.value())
    mdify_status= 0
    if modfiyable ==1:
        # only modify while has wall on right
        for i in range(0,10):
            # base on the distance to the wall to modify its track
            sleep(0.1) # at the branch could be modify
            if usL.value()<60:
                # too close to the wall
                break
            # 80 and 120 should be modify
            if usR.value()*10 <100:
                if mdify_status !=1:
                    mdify_status =1
                    print("modify to turn left")
                    motor_move(250,300)
            elif usR.value()*10 > 140:
                if mdify_status !=2:
                    mdify_status =2
                    print("modify to turn right")
                    motor_move(300,250)
            else :
                if mdify_status !=3:
                    mdify_status =3
                    motor_move()
    # ordinary move forward
    motor_move()
    while rightMotor.position>to_distance and (not btn.any()) and is_color==0 and usL.value()>60:
        sleep(0.01)
        if cs.value()== can_color:
            motor_stop()
            sleep(0.1)
            if cs.value()== can_color:
                is_color=1
            else:
                motor_move()
        else:
            motor_move()

    motor_stop()




if __name__ == '__main__':
    print("finished initialisation -- Press a Key to start")
    # main method
    while (not btn.any()) and  is_color== 0:
        """ordinary movement by cor"""
        if tree.find_node(x,y)=='NULL':
            this_node= tree.add_node(x,y,is_wall('f'),is_wall('l'),is_wall('r'),head_dir)
        else :
            this_node = tree.find_node(x,y)
        this_node.print_node()
        to_dir =this_node.move_to(head_dir)
        turn(to_dir)
        cor_move(head_dir,-is_wall('r'))

    """code after found the can"""

    print("find the red can")
    # sound the alarm of found the can
    Sound.tone([(1000, 500, 500)] * 3)
    motor_move()
    sleep(0.3)
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
    to_dir = this_node.move_to(head_dir)
    #turn 180 degree
    turn(to_dir)
    #refresh the cordinate by a low level func so it won't move
    refresh_cor(head_dir)

    # reset the is_color value so it could move back
    is_color = 0

    """ revise its route """
    print("now is retreat it's route")
    while (x!=0 or y!=0) and not btn.any() :
        this_node = tree.find_node(x,y)
        this_node.print_node()
        to_dir =this_node.back_to(head_dir)
        turn(to_dir)
        print ("here is",x,",",y)

        cor_move(head_dir,-is_wall('r'))
        print ("next dir is",head_dir)

    print("finally here is:",x,",",y)

    motor_stop()
    print("end of the programme")
