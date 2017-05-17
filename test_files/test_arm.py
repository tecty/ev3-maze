from ev3dev.ev3 import *
from time import sleep


turnMotor = LargeMotor(OUTPUT_D)

turnMotor.run_forever(speed_sp=-300)
sleep(0.5)
turnMotor.stop()
turnMotor.run_forever(speed_sp= 0)
