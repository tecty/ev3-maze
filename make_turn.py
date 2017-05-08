#!usr/bin/env python3
from ev3dev.ev3 import *
from time import sleep


gy = GyroSensor()

gy.mode = 'GYRO-ANG'

leftMotor = LargeMotor('outB')
rightMotor = LargeMotor('outC')

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
    gy.mode = 'GYRO-RATE'
    gy.mode = 'GYRO-ANG'

    # print("*",gy.value())
    #make a turn
    leftMotor.run_forever(speed_sp = direction * turning_speed *(-1))
    rightMotor.run_forever(speed_sp = - direction * turning_speed *(-1))

    while gy.value() * direction < angle:
        # print(gy.value())
        sleep(0.005)

    rightMotor.stop()
    leftMotor.stop()

    # print("*", gy.value())

    while gy.value() * direction > angle:
        leftMotor.run_forever(speed_sp = direction * reversing_speed)
        rightMotor.run_forever(speed_sp = - direction * reversing_speed)
        # print(gy.value())
        sleep(0.005)

    rightMotor.stop()
    leftMotor.stop()

    # print("*",gy.value())

    head_dir = to_dir
    return 1

btn = Button()
flag = 0
while not btn.any():
    if flag == 0:
        head_dir = 270
        turn(0)
        # print("head_dir:", head_dir)
#        makeTurn(-1, 90, 500, 200, 200)
#        makeTurn(-1, 180, 0, 200, 200)
        flag = 1

rightMotor.stop()
leftMotor.stop()
