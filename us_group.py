#!/usr/bin/python3
from time import sleep
from ev3dev.ev3 import *

class us_group(self):
    """docstring for us_group."""
    def __init__(self):
        super(us_group, self).__init__()
        # assign mode, 0 is forward, 1 is backward
        self.__mode= 0

        # the status of the motor dir
        self.motor_dir =0
        # critical values of detecting walls
        self.sonar_sum = 340
        self.wall_distance  = 280
        self.front_wall_dis = 280
        # assign motor
        self.motor  = MediumMotor(OUTPUT_D)
        # assign sensor
        self.usR = UltrasonicSensor(INPUT_1);	assert usR.connected
        self.usL = UltrasonicSensor(INPUT_2);	assert usL.connected

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

    def is_wall(self):
        # detecting front
        self.turn(0)
        front = self.usL.value()
        # detecting left and right
        self.turn(90)
        left  = self.usL.value()
        right = self.usR.value()

        """calculate the return result"""
        # front
        if front < self.front_wall_dis:
            front = -1
        else:
            front =  0
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
        if self.usR.value()<wall_distance:
            # now have wall on its right
            """ Values should be modify"""
            if self.usR.value()*10>140:
                return 1
            elif self.usR.value()*10<100:
                return -1
        return 0
    def is_front(self,front_dis=60):
        # detect whether is a wall at front

        self.turn(0)
        if self.usL.value()<front_dis:
            return 1
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
        if test_fucntion == "turn":
            while True:
                to_dir = input("Direction:(0/90)")
                if to_dir == "0" or "90":
                    usg.turn(to_dir)
                    next_turn = input("Test another direction?(y/n)")
                    if(next_turn == "n" or "N"):
                        break
                else:
                    print("Wrong direction")
        elif test_function ==  "is_wall":
            while not btn.any():
                d = usg.is_wall()
                print("Front:",d[0],"Left:",d[1],"Right:",d[2])
                sleep(0.1)
        elif test_function == "modify_dir":
            while not btn.any():
                move_dir = usg.modify_dir()
                if move_dir == 1:
                    print("Move right")
                elif move_dir == -1:
                    print("Move left")
                else:
                    print("No move")
                sleep(0.1)
        else:
            print("No such function exist")
        test = input("Test other function?(y/n)")
        if test == "n" or "N":
            break
