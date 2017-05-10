from cor_Aki import *
print("finished initialisation")
while (not btn.any()) and is_color== 0:
    cor_move(head_dir)

print("find the red can")
# sound the alarm of found the can
Sound.tone([(1000, 500, 500)] * 3)
# revise to the last node
motor_move(-200,-200)
print("old position is",rightMotor.position,"before_distance is",before_distance)
while (not btn.any()) and rightMotor.position<before_distance:
    sleep(0.01)
motor_stop()

print("end of the programme")
