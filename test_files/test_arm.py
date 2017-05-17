from ev3dev.ev3 import *
from time import sleep


turnMotor = MiddleMotor(OUTPUT_D)

turnMotor.run_forever(speed_sp=300)
sleep(1)
turnMotor.stop()
turnMotor.run_forever(speed_sp= 0)
