#!/usr/bin/python3
from cor_Aki import *


print("finished initialisation")
while not btn.any():
    approach_wall()
    cor_move(head_dir )
    modify_angle()

    sleep(1.5)
print("End of the programme")

motor_stop()
