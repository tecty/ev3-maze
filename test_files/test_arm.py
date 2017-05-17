from ev3dev.ev3 import *


turnMotor = MiddleMotor(OUTPUT_D)

turnMotor.run_forever(speed_sp=300)
turnMotor.stop()
turnMotor.run_forever(speed_sp= 0)
