#!/usr/bin/python3
from time import sleep
from ev3dev.ev3 import *
from tree_list import *
from us_group import *
liftMotor  = LargeMotor(OUTPUT_A); assert liftMotor.connected
leftMotor  = LargeMotor(OUTPUT_B); assert leftMotor.connected
rightMotor = LargeMotor(OUTPUT_C); assert rightMotor.connected

gs  = GyroSensor(INPUT_4);	assert gs.connected
cs  = ColorSensor(INPUT_3);	assert cs.connected
btn = Button()
cs.mode = 'COL-COLOR'

"""new define class of UltrasonicSensor"""
usg=us_group()

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
# sign of last time whether it is stop by is front
front_wall_break =0
# store whether the sensor detected red color
is_color=0
# determin whether it has catch the can
is_catch =0
# initialisation the tree var
tree = Tree()


"""config part these values should be modify """
# length of one unit
# unit_length=830 # for clancy in normal speed
unit_length=900 # for fast speed
# unit_length=870 # for E4
# the color of the can 5 is red
can_color =5
# speed that motor run in default
default_sp=300

"""defined in us_group"""
# theshold of detecting a wall
# wall_distance= 280


def motor_move(leftSpeed=default_sp,rightSpeed=default_sp+10):
    rightMotor.run_forever(speed_sp=rightSpeed)
    leftMotor.run_forever(speed_sp=leftSpeed)

def motor_stop():
    leftMotor.stop()
    rightMotor.stop()
    motor_move(0,0)

def catch_can():
    global is_catch
    liftMotor.run_forever(speed_sp =-100)
    sleep(1)
    liftMotor.stop()
    # set the robot that have catch the can
    is_catch =1
    liftMotor.run_forever(speed_sp=-50)
def stop_catch():
    liftMotor.stop()
    liftMotor.run_forever(speed_sp=0)

"""manipulate the coordinate"""
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
def turn(to_dir):
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
    motor_move(direction*default_sp,-direction*default_sp)

    while gs.value() * direction < angle:
        sleep(0.005)

    motor_stop()
    sleep(0.1)

    # revise to the angle that wanted # revise speed is 30
    motor_move(-direction*30,direction*30)
    while gs.value() * direction > angle:
        sleep(0.005)

    motor_stop()
    sleep(0.1)

    head_dir = to_dir

    # update the last_distance to usg,
    # because it have been changed its relative wall position
    usg.set_last_distance(usg.accur_us())
    return 1

"""try to approach the center by the distance to a wall"""
def approach_wall():
    if front_wall_break:
        # if front has wall, try to approach the wall at front
        approach_move()

    wall_dir= usg.is_approach_wall()
    print("is_approach = ", wall_dir)
    print("usL =",usg.last_distance[0],"usR =", usg.last_distance[1])
    if wall_dir == 0:
        # dont need to do anything
        return 0
    elif wall_dir == 1:
        # wall is on the right
        to_dir = head_dir+90
    elif wall_dir == -1:
        # wall is on the left
        to_dir = head_dir-90


    """special case of to_dir"""
    if to_dir==-90:
        to_dir =270
    elif to_dir == 360:
        to_dir = 0
    print("trying to trun to ", to_dir,"to approach wall")
    # turn to that direction that have a wall
    turn(to_dir)
    #  after turned, couldn't detect the can, to prevent unexpected error
    approach_move(1)

def approach_move(catched = is_catch):
    global is_color
    print("trying to approach the wall")
    # set the us sensor to the front
    usg.turn(0)
    """ Values need to be modify """
    while usg.usL.value() < 160:
        motor_move(-100,-100)
        sleep(0.02)
    while usg.usL.value() > 170:
        motor_move(100,100)
        # only when it try to approach the wall at front, can have the can to detect
        if cs.value()== can_color and catched ==0:
            motor_stop()
            sleep(0.1)
            if cs.value()== can_color:
                is_color=1
                # break this loop
                break
        else:
            sleep(0.1)

    motor_stop()

def modify_angle():

    if abs(usg.angle)>=1:
        # try to modify by the angle
        print("modify for angle", usg.angle)
        gs.mode = 'GYRO-RATE'
        gs.mode = 'GYRO-ANG'
        if usg.angle>0:
            direction = 1
        else:
            direction = -1

        # start modify the angle
        motor_move(-direction * 30,direction * 30)
        while abs(gs.value()) < abs(usg.angle):
            sleep(0.005)
        # end of this modify
        motor_stop()

        # set the accur_us after modify into usg
        usg.set_last_distance(usg.accur_us())


# test cor_move
def cor_move(head_dir):
    global before_distance, is_color, front_wall_break
    # refresh the global cordinate by its head direction
    refresh_cor(head_dir)
    # record the position before it move forward
    before_distance = rightMotor.position
    to_distance = rightMotor.position+unit_length
    print("to_distance = ",to_distance,"unit_length=",unit_length)
    mdify_status= 0
    # front wall break would set to 0
    front_wall_break = 0

    motor_move()
    while  rightMotor.position< to_distance and is_color == 0:
        if usg.is_front():
            # set the front_wall_break to 1, so approach front would work
            front_wall_break = 1;
            break
        if cs.value()== can_color and is_catch ==0:
            motor_stop()
            sleep(0.1)
            if cs.value()== can_color:
                is_color=1
                break
        else:
            sleep(0.1)
    motor_stop()




if __name__ == '__main__':
    print("finished initialisation -- Press a Key to start")
    # main method
    while (not btn.any()) and  is_color== 0:
        """ordinary movement by cor"""
        if tree.find_node(x,y)=='NULL':
            this_node= tree.add_node(x,y,usg.is_wall(),head_dir)
        else :
            this_node = tree.find_node(x,y)
            # redo the usg.is_wall, so that it would calculate the new angle
            usg.is_wall()
        this_node.print_node()
        # know what dir to go for next node
        to_dir =this_node.move_to(head_dir)
        print("next dir is ", to_dir,"head dir",head_dir)
        # at this_node, try to modify robot's angle
        modify_angle()

        # modify to the center of that node
        approach_wall()
        # turn to the direction of next node
        turn(to_dir)



        print("next dir is ", to_dir,"head dir",head_dir)
        cor_move(head_dir)



    """code after found the can"""
    print("find the red can")
    # sound the alarm of found the can
    Sound.tone([(1000, 500, 500)] * 3)

    # reach the can
    motor_move()
    sleep(0.3)
    motor_stop()
    # catch the can
    catch_can()

    # set the node for the can at.
    if tree.find_node(x,y):
        this_node= tree.add_node(x,y,[-1,-1,-1],head_dir)
    else :
        this_node = tree.find_node(x,y)
    this_node.print_node()

    # revise to the last node
    motor_move(-200,-200)
    print("old position is",rightMotor.position,"before_distance is",before_distance)
    while (not btn.any()) and rightMotor.position>before_distance:
        sleep(0.05)
    motor_stop()

    # now is at the node before
    to_dir = this_node.move_to(head_dir)
    #turn 180 degree
    turn(to_dir)
    #refresh the cordinate by a low level func so it won't move
    refresh_cor(head_dir)

    # refresh the last_distance so the robot can modify its angle at next node
    usg.set_last_distance(usg.accur_us())

    # reset the is_color value so it could move back
    is_color = 0

    """ revise its route """
    print("now is retreat it's route")
    while (x!=0 or y!=0) and not btn.any() :
        # tring to find out the modify angle
        usg.is_wall()
        this_node = tree.find_node(x,y)
        this_node.print_node()
        to_dir =this_node.back_to(head_dir)

        """modify the position to that unit"""
        # trying to modify_angle
        modify_angle()
        # trying to modify the distance to wall
        approach_wall()

        turn(to_dir)
        print ("here is",x,",",y)

        cor_move(head_dir,1)
        modify_angle()
        print ("next dir is",head_dir)

    print("finally here is:",x,",",y)


    # finally stop the robot
    motor_stop()
    stop_catch()
    print("end of the programme")
