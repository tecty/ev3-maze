#!/usr/bin/python3
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
# store whether the sensor detected red color
is_color=0
# initialisation the tree var
tree = Tree()

"""config part these values should be modify """
# length of one unit
# unit_length=830 # for clancy in normal speed
unit_length=1050 # for clancy in normal speed
# unit_length=870 # for E4
# the color of the can 5 is red
can_color =5
# speed that motor run in default
default_sp=250

"""defined in us_group"""
# theshold of detecting a wall
# wall_distance= 280


def motor_move(leftSpeed=default_sp,rightSpeed=default_sp):
    leftMotor.run_forever(speed_sp=leftSpeed)
    rightMotor.run_forever(speed_sp=rightSpeed)

def motor_stop():
    leftMotor.stop()
    rightMotor.stop()
    motor_move(0,0)

def catch_can():
    liftMotor.run_forever(speed_sp =-100)
    sleep(1)
    liftMotor.stop()
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
    return 1

"""try to approach the center by the distance to a wall"""
def approach_wall():
    wall_dir= usg.is_approach_wall()
    print("is_approach = ", wall_dir)
    print("usL =",usg.usL.value(),"usR =", usg.usR.value()*10)
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
    print("trying to trun to ", to_dir)
    # turn to that direction that have a wall
    turn(to_dir)
    # set the us sensor to the front
    usg.turn(0)

    print(" trying to approach the wall")

    """ Values need to be modify """
    while usg.usL.value() < 160:
        motor_move(-100,-100)
        sleep(0.02)
    while usg.usL.value() > 170:
        motor_move(100,100)
        sleep(0.02)
    motor_stop()

def modify_angle():

    if abs(usg.angle)>3 :
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
def cor_move(head_dir,is_catch =0):
    global before_distance, is_color
    # refresh the global cordinate by its head direction
    refresh_cor(head_dir)
    # record the position before it move forward
    before_distance = rightMotor.position
    to_distance = rightMotor.position+unit_length
    print("to_distance = ",to_distance,"unit_length=",unit_length)
    mdify_status= 0

    motor_move(520,500)

    """stage 1: fast move"""
    while usg.is_front()!=1 and rightMotor.position< to_distance-100 and is_color == 0:
        if cs.value()== can_color and is_catch ==0:
            motor_stop()
            sleep(0.1)
            if cs.value()== can_color:
                is_color=1

    """stage 2: slow move"""
    motor_move()
    while usg.is_front()!=1 and rightMotor.position< to_distance and is_color == 0:
        if cs.value()== can_color and is_catch ==0:
            motor_stop()
            sleep(0.1)
            if cs.value()== can_color:
                is_color=1
    motor_stop()

usg=us_group()

# set the info of first node
usg.set_last_distance(usg.accur_us())
print("finished initialisation")
while not btn.any():
    usg.is_wall()
    # modify_angle of this node
    modify_angle()
    cor_move(head_dir)
    print("finished one cor_moves")
    sleep(3)
print("End of the programme")

motor_stop()
