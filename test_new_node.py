from cor_Aki import *
print("finished initialisation")
while not btn.any():
    this_node= tree.add_node(x,y,is_wall('f'),is_wall('l'),is_wall('r'),head_dir)
    this_node.print_node()
    sleep(2)

print("end of the programme")
