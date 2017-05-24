from cor_Aki import *
# initial the angle of sensor
print("finished initialisation")
while  not btn.any():
    print("start catching ")
    catch_can()
    print("stop catching")
    stop_catch()
    sleep(2)

print("end of the programme")
