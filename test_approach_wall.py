from cor_Aki import *
# initial the angle of sensor

print("finished initialisation")
while  not btn.any():
    # trying to approach the wall at front
    approach_wall()
    turn(0)
    sleep(2)


print("end of the programme")
