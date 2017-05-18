from cor_Aki import *
# initial the angle of sensor
usg=us_group()
usg.turn(90)
print("finished initialisation")
while  not btn.any():
    print("usL =",usg.usL.value(),"usR =", usg.usR.value()*10, "sum =",usg.usL.value()+usg.usR.value()*10)
    sleep(2)

print("end of the programme")
