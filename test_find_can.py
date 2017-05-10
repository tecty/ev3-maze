from cor_Aki import *
print("finished initialisation")
while not btn.any() and cs.value() != can_color:
    cor_move(head_dir)

print("find the red can")
# sound the alarm of found the can
Sound.tone([(1000, 500, 500)] * 3)


print("end of the programme")
