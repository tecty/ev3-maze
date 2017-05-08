#!usr/bin/env python3
from ev3dev.ev3 import *
from time import sleep


sonarMotor = MediumMotor('outD')

#to_dir 0 - front, 90 - left
def us_turn(to_dir, turning_speed = 250, reversing_speed = 40):

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

btn = Button()
flag = 0
while not btn.any():
    if flag == 0:
        # print("*1",sonarMotor.position)
        us_turn(90)
        flag = 1
    if flag == 1:
        # print("*2",sonarMotor.position)
        us_turn(0)
        flag = 0

# print("*",sonarMotor.position)
sonarMotor.stop()
