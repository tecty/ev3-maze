from cor_Aki import *
# initial the angle of sensor

print("finished initialisation")
while  not btn.any():
    # trying to approach the wall at front
    # refresh the accur value
    usg.set_last_distance(usg.accur_us())
    # try to approach_wall
    approach_wall()
    turn(0)
    sleep(2)


print("end of the programme")
