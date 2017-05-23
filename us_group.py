#!/usr/bin/python3
from time import sleep
from ev3dev.ev3 import *
from math import *

class us_group:
    """docstring for us_group."""
    def __init__(self):
        super(us_group, self).__init__()
        # assign mode, 0 is forward, 1 is backward
        self.__mode= 0

        # the status of the motor dir
        self.motor_dir =34
        """These values should be modify"""
        # critical values of detecting walls
        self.sonar_sum = 280
        self.wall_distance  = 250
        self.front_wall_dis = 220
        # assign motor
        self.motor  = MediumMotor(OUTPUT_D);	assert self.motor.connected
        # assign sensor
        self.usL = UltrasonicSensor(INPUT_2);	assert self.usL.connected
        self.usR = UltrasonicSensor(INPUT_1);	assert self.usR.connected

        # modify angle
        self.last_distance = [-1,-1]
        self.modify_distance = 20
        self.angle = 0
        self.modify_direction = 0 #-1 - left, 1 - right


    def turn(self,to_dir):
        pos = [0,-90]
        if self.motor_dir!=to_dir:
            self.motor_dir = to_dir
        else:
            # success turning the motor because motor was at the site it need to be
            return 1

        """ turn to the given position """
        if to_dir == 0:
            distance = pos[0]
        elif to_dir == 90:
            distance = pos[1]
        start = self.motor.position
        # run the motor
        self.motor.run_to_abs_pos(position_sp = distance, speed_sp = 250, stop_action = "brake")

        # sleep till the motor is not moving
        while self.motor.state:
            sleep(0.01)
        sleep(0.1)

    def is_wall(self):
        # detecting front
        front = -self.is_front()
        # detecting accur left and right distance
        accur_val = self.accur_us()
        # calculate the modify_angle from this accur_val
        self.modify_angle(accur_val);

        """calculate the return result"""
        # left and right
        if accur_val[0] +  accur_val[1] < self.sonar_sum:
            left  = -1
            right = -1
        else:
            if accur_val[0]  < self.wall_distance:
                left = -1
            else:
                left =  0
            if accur_val[1]  < self.wall_distance:
                right = -1
            else:
                right = 0

        # after calculate is wall, set the val into this obj
        self.set_last_distance(accur_val);

        # return the wall info by array
        return [front,left,right]

    """
    return the accurate value of us [0] = left_accur
                                    [1] = right_accur"""
    def accur_us(self):
        # array[5][2]
        self.turn(90)
        source_data =[[],[]] # length is 5 width is 2
        for i in range(0,6):
            # get 5 source_data in to list
            source_data[0].append(self.usL.value())
            source_data[1].append(self.usR.value()*10)
            sleep(0.05)
        # calculate the accurate data that has been detect
        left_accur = (sum(source_data[0])-max(source_data[0]) -min(source_data[0])) / float(len(source_data[0])-2)
        right_accur = (sum(source_data[1])-max(source_data[1])-min(source_data[1]) )/ float(len(source_data[1])-2)
        return [left_accur,right_accur]
    def modify_dir(self):
        """move to right is 1, move to left is -1"""
        if self.usR.value()*10<self.wall_distance:
            # now have wall on its right
            """ Values should be modify"""
            if self.usR.value()*10>140:
                return 1
            elif self.usR.value()*10<100:
                return -1
        if self.usL.value()<self.wall_distance and self.motor_dir == 90:
            # now have wall on its left
            # note: because it is on otherside, to the dir
            # is oppisite from above
            """ Values should be modify"""
            if self.usL.value()>140:
                return -1
            elif self.usL.value()<100:
                return 1
        return 0


    def is_approach_wall(self):
        # set the sensor to 90
        self.turn(90)
        """approach the wall of right 1, move to left is -1"""
        if self.usL.value()<self.wall_distance :
            # now have wall on its left
            # determine whether it would approach to left
            """ Values should be modify"""
            if self.usL.value()>165: #
                return -1
            elif self.usL.value()<80: # 50 ?
                return -1
        if self.usR.value()*10<self.wall_distance:
            # now have wall on its right
            """ Values should be modify"""
            if self.usR.value()*10>200:
                return 1
            elif self.usR.value()*10<100: # 70?
                return 1
        return 0

    def is_front(self):
        # detect whether is a wall at front
        self.turn(0)
        if self.usL.value()<self.front_wall_dis:
            sleep(0.1)
            # double check the front wall
            if self.usL.value()<self.front_wall_dis:
                print("front has wall")
                return 1
            else:
                return 0
        else:
            return 0

    def set_last_distance(self, accur_val):
        for i in range(0,2):
            if accur_val[i]> self.wall_distance:
                #  if detect the branch, set the last_distance into -1
                self.last_distance[i]=-1
            else:
                self.last_distance[i]= accur_val[i]

    def modify_angle(self,accur_val):
        for i in range(0,2):
            if self.last_distance[i] ==-1:
                # set the angle, prevent the for that dosn't calculate the angle
                self.angle = 0
            else :
                diff =pow(-1,i)* (accur_val[i] - self.last_distance[i])
                # calculate the angle would be modify
                print("diff new is ",diff)
                self.angle = asin(diff/420)*60
                print("Angle would be modify is", self.angle);
                # break this loop so the angle wouldn't calculate twice
                break




    """unneccessary code"""
    @property
    def mode(self):
        return self.__mode
    @mode.setter
    def mode(self,value):
        self.__mode=value

if __name__ == '__main__':
    """unit test for us_group"""
    usg = us_group()
    btn = Button()



    while True:
        test_function = input("Testing function name(turn/is_wall/modify_dir): ")
        if test_function == "turn":
            while not btn.any():
                to_dir = input("Direction:(0/90)")
                if to_dir == "0" or "90":
                    usg.turn(to_dir)
                else:
                    print("Wrong direction")
                sleep(0.5)
        elif test_function ==  "is_wall":
            while not btn.any():
                d = usg.is_wall()
                print("Front:",d[0],"Left:",d[1],"Right:",d[2])
                sleep(1)
        elif test_function == "modify_dir":
            while not btn.any():
                move_dir = usg.modify_dir()
                if move_dir == 1:
                    print("Move right")
                elif move_dir == -1:
                    print("Move left")
                else:
                    print("No move")
                sleep(1)
        else:
            print("No such function exist")
