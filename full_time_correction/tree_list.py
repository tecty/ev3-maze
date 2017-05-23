#!/usr/bin/python3

class Tree:
    """docstring for tree."""
    def __init__(self):
        self.nodes=list()
    def add_node(self,x,y,wall_list,head_dir):
        # input left,right is 0(has a way) or -1(wall)
        # wall_list : [0] - front, [1] - left, [2] - right
        if head_dir ==0:
            this_node= Node(x,y,wall_list[0],wall_list[2],0,wall_list[1])
        if head_dir ==90:
            this_node= Node(x,y,wall_list[1],wall_list[0],wall_list[2],0)
        if head_dir ==180:
            this_node= Node(x,y,0,wall_list[1],wall_list[0],wall_list[2])
        if head_dir ==270:
            this_node= Node(x,y,wall_list[2],wall_list[0],wall_list[1],0)
        self.nodes.append(this_node)
        return this_node
    def find_node(self,x,y):
        for node in self.nodes:
            if node.cor[0] == x and node.cor[1] == y:
                return node
        return 'NULL'


class Node:
    def __init__(self,x,y,dir0,dir90,dir180,dir270):
        self.cor= [x,y]
        self.branch=[dir0,dir90,dir180,dir270]
    def get_next_dir(self):
        # to record the count in the branch
        min_dir_count = 10
        # to auto increase while scan in branch
        direction = 0
        # to record the direction that min_dir_count at
        min_dir = 0
        for count_branch in self.branch:
            if min_dir_count> count_branch and count_branch >=0:
                min_dir = direction
                min_dir_count = count_branch
            direction += 90
        return min_dir
    def print_node(self):
        print("cor =", self.cor,"branch =", self.branch)
    def move_to(self,head_dir):
        # add one on where it from
        self.branch[int(head_dir/90+2)%4]+=1
        next_dir = self.get_next_dir()
        # add one on where it to
        self.branch[int(next_dir/90)]+=1
        return next_dir
    def back_to(self,head_dir):
        #refresh the correct cordinate in case it would go back to where it from
        self.branch[int(head_dir/90+2)%4]+=1

        # to record the count in the branch
        back_dir_count = 10
        # to auto increase while scan in branch
        direction = 0
        # to record the direction that back_dir_count at
        back_dir = 0

        self.print_node
        for count_branch in self.branch:
            if back_dir_count> count_branch and count_branch >=1:
                # ignore the branch that haven't visit
                back_dir = direction
                back_dir_count = count_branch
            direction += 90

        # refresh the branch of it would go to
        self.branch[int(back_dir/90)]+=1
        return back_dir


if __name__ == '__main__':

    x=0
    y=0
    def cor_move(head_dir):
        global x,y
        if head_dir == 0:
            y+=1
        elif head_dir==90:
            x+=1
        elif head_dir==180:
            y-=1
        elif head_dir==270:
            x-=1
    tree = Tree()
    head_dir = 0
    if tree.find_node(x,y)=='NULL':
        this_node= tree.add_node(0,0,[0,-1,-1],head_dir)
    else :
        this_node = tree.find_node(0,0)
    head_dir =this_node.move_to(0)
    print ("next dir is",head_dir)
    this_node.print_node()
    cor_move(head_dir)

    print ("head_dir = ",head_dir)
    this_node= tree.add_node(x,y,[-1,-1,0],head_dir)
    head_dir =this_node.move_to(head_dir)
    cor_move(head_dir)
    this_node.print_node()
    print ("next dir is",head_dir)
    this_node= tree.add_node(x,y,[-1,-1,0],head_dir)
    head_dir =this_node.move_to(head_dir)
    cor_move(head_dir)
    this_node.print_node()
    print ("next dir is",head_dir)
    this_node= tree.add_node(x,y,[-1,-1,-1],head_dir)
    head_dir =this_node.move_to(head_dir)
    cor_move(head_dir)
    this_node.print_node()
    print ("next dir is",head_dir)


    print ("\nrevise robot")
    # reversing the route
    while x!=0 or y!=0:
        this_node = tree.find_node(x,y)
        head_dir=this_node.back_to(head_dir)
        this_node.print_node()
        cor_move(head_dir)
        print ("next dir is",head_dir)
    print(x,",",y)
