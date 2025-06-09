from controller_reader import LeftStickXReader 
from motor_driver import Motor
from servo_driver import Servo
import time
import subprocess

#used modules
reader = LeftStickXReader()
motor = Motor()
servo = Servo()

#gloabal variables
current_angle = 0
target_angle = 0


def move_motor():
    global current_angle, target_angle, motor

    clock_wise = target_angle > current_angle

    if(clock_wise):
        motor.rotate_motor_single_step(False)
        current_angle += Motor.convert_step_count_to_angle(1)  
    else:
        motor.rotate_motor_single_step(True)
        current_angle -= Motor.convert_step_count_to_angle(1)  
    
    time.sleep(motor.MIN_DELAY_TIME)

#main program ---------------------------------------------------------------------------------

try:
    while True:
        target_angle = reader.get_left_stick_angle()
        #move the stepper motor
        move_motor()
        #move the servo motor
        servo.set_servo(target_angle)
        print(f"Current Angle Stepper Motor: {current_angle:.2f} Target Angle: {target_angle}")

except KeyboardInterrupt:
    print("Exiting...")
finally:
    reader.close()