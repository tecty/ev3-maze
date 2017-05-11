from cor_Aki import *

us_turn(90)
print("finished initialisation")
while  not btn.any():
    print("usL =",usL.value(),"usR =", usR.value()*10, "sum =",usL.value()+usR.value()*10)
    sleep(2)

print("end of the programme")
