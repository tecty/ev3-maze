from cor_Aki import *
# initial the angle of sensor
usg=us_group()
usg.turn(90)
print("finished initialisation")
while  not btn.any():
    is_approach= usg.is_approach_wall()
    print("is_approach = ", is_approach)
    # trying to approach the wall at front
    approach_wall()

    turn(0)
    sleep(2)


print("end of the programme")
