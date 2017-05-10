from cor_Aki import *
print("finished initialisation")
while (not btn.any()) and  is_color== 0:
    """ordinary movement by cor"""
    if tree.find_node(x,y)=='NULL':
        this_node= tree.add_node(x,y,is_wall('f'),is_wall('l'),is_wall('r'),head_dir)
    else :
        this_node = tree.find_node(x,y)
    this_node.print_node()
    to_dir =this_node.move_to(head_dir)
    turn(to_dir)
    cor_move(head_dir)

"""code after found the can"""

print("find the red can")
# sound the alarm of found the can
Sound.tone([(1000, 500, 500)] * 3)
# set the node for the can at.
if tree.find_node(x,y)=='NULL':
    this_node= tree.add_node(x,y,-1,-1,-1,head_dir)
else :
    this_node = tree.find_node(x,y)
this_node.print_node()

# revise to the last node
motor_move(-200,-200)
while not btn.any() and usL.value()<before_distance:
    sleep(0.1)
motor_stop()

# now is at the node before
to_dir = this_node.move(head_dir)
#turn 180 degree
turn(to_dir)
#refresh the cordinate by a low level func so it won't move
refresh_cor(head_dir)

# revise its route
print("now is retreat it's route")
while (x!=0 or y!=0) and not btn.any() :
    this_node = tree.find_node(x,y)
    this_node.print_node()
    to_dir =this_node.back_to(head_dir)
    turn(to_dir)
    cor_move(head_dir)
    print ("next dir is",head_dir)

print("finally here is:",x,",",y)

motor_stop()
print("end of the programme")




print("end of the programme")
