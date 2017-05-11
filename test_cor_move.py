from cor_Aki import *


print("finished initialisation")
while not btn.any():
    cor_move(head_dir,1 )
    print("the distance to the wall befor cor_move", before_distance)
    print("new cordinate now is [",x,y,"]")
print("End of the programme")

motor_stop()
