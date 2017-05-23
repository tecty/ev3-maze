from cor_Aki import *
# initial the angle of sensor
usg=us_group()
usg.turn(90)
print("finished initialisation")
while  not btn.any():
    accur_val= usg.accur_us()
    print("usL =",accur_val[0],"usR =", accur_val[1])
    sleep(2)

print("end of the programme")
