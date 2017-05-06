from ev3dev.ev3 import *


turnMotor = MiddleMotor(OUTPUT_D)

turnMotor.run_direct(duty_cycle_sp= 25)
