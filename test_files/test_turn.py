from cor_Aki import *
# initial the angle of sensor

print("finished initialisation")
while  not btn.any():
    turn(90)
    print("turn to 90")
    sleep(2)
    turn(180)
    print("turn to 180")
    sleep(2)
    turn(270)
    print("turn to 270")
    sleep(2)
    turn(90)
    print("turn to 90")
    sleep(2)
    turn(0)
    print("turn to 0")
    sleep(2)
print("end of the programme")
