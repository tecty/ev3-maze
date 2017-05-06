from ev3dev.ev3 import *
from time import sleep


turnMotor = MediumMotor(OUTPUT_D)

turnMotor.run_direct(duty_cycle_sp= 100)
sleep(0.03)
turnMotor.stop()
