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
us1  = UltrasonicSensor(INPUT_1);	assert us1.connected
us2  = UltrasonicSensor(INPUT_2);	assert us2.connected
btn = Button()
cs.mode = 'COL-COLOR'

def motor_move(leftSpeed=300,rightSpeed=300):
	leftMotor.run_forever(speed_sp=-leftSpeed)
	rightMotor.run_forever(speed_sp=-rightSpeed)
status=0

# cordinate of robot's postion
x = 0
y = 0
# face direction of robot
head_dir = 0


turn(to_dir)

print ('finished initialisation')
while not btn.any():
    sleep(0.1)
#start the main programme

while not btn.any():
    if us1.value()>100 or us2.value()>100:
        # found a branch
        if status!=1:
            status=1
            sleep(0.5)

            motor_move(-1000,-1000)
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
