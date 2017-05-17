from ev3dev.ev3 import *
from time import sleep


turnMotor = MiddleMotor(OUTPUT_D)

turnMotor.run_forever(speed_sp=300)
turnMotor.stop()
sleep(1)
turnMotor.run_forever(speed_sp= 0)
