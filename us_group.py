#!/usr/bin/python3
from time import sleep
from ev3dev.ev3 import *

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
        self.front_wall_dis = 120
        # assign motor
        self.motor  = MediumMotor(OUTPUT_D);	assert self.motor.connected
        # assign sensor
        self.usL = UltrasonicSensor(INPUT_2);	assert self.usL.connected
        self.usR = UltrasonicSensor(INPUT_1);	assert self.usR.connected

    def turn(self,to_dir):
        pos = [1,-89]
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
        if distance == 0: return 0
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
        # detecting left and right
        self.turn(90)
        left  = self.usL.value()
        right = self.usR.value()*10

        """calculate the return result"""
        # left and right
        if left + right < self.sonar_sum:
            left  = -1
            right = -1
        else:
            if left  < self.wall_distance:
                left = -1
            else:
                left =  0
            if right < self.wall_distance:
                right = -1
            else:
                right = 0
        return [front,left,right]
    def modify_dir(self):
        """move to right is 1, move to left is -1"""
        if self.usR.value()*10<self.wall_distance:
            # now have wall on its right
            """ Values should be modify"""
            if self.usR.value()*10>140:
                return 1
            elif self.usR.value()*10<100:
                return -1
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
