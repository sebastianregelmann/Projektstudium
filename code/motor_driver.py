#!/usr/bin/python3
import RPi.GPIO as GPIO

import time


class Motor:

    def __init__(self, controller_index=0): 
        self.MOTOR_PINS = [17,18,27,22]
        self.STEP_SEQUENCE = [[1,0,0,1],
                    [1,0,0,0],
                    [1,1,0,0],
                    [0,1,0,0],
                    [0,1,1,0],
                    [0,0,1,0],
                    [0,0,1,1],
                    [0,0,0,1]]

        self.MIN_DELAY_TIME = 0.005
  
        self.setup()
        print("Motor setup")
    
    
    def setup(self):
        global motor_step_counter
        # setting up
        GPIO.setmode( GPIO.BCM )
        GPIO.setup(self.MOTOR_PINS[0], GPIO.OUT )
        GPIO.setup(self.MOTOR_PINS[1], GPIO.OUT )
        GPIO.setup(self.MOTOR_PINS[2], GPIO.OUT )
        GPIO.setup(self.MOTOR_PINS[3], GPIO.OUT )

        # initializing
        GPIO.output(self.MOTOR_PINS[0], GPIO.LOW )
        GPIO.output(self.MOTOR_PINS[1], GPIO.LOW )
        GPIO.output(self.MOTOR_PINS[2], GPIO.LOW )
        GPIO.output(self.MOTOR_PINS[3], GPIO.LOW )
        
        #set counter to 0
        self.motor_step_counter = 0 


    def cleanup(self):
        GPIO.output(self.MOTOR_PINS[0], GPIO.LOW )
        GPIO.output(self.MOTOR_PINS[1], GPIO.LOW )
        GPIO.output(self.MOTOR_PINS[2], GPIO.LOW )
        GPIO.output(self.MOTOR_PINS[3], GPIO.LOW )
        GPIO.cleanup()


    #moves the motor one step in one direction
    def rotate_motor_single_step(self, clock_wise):
        if clock_wise==True:
            self.motor_step_counter = (self.motor_step_counter - 1) % 8
        else:
            self.motor_step_counter = (self.motor_step_counter + 1) % 8
        #loop over the pins and move the motor
        for pin in range(0, len(self.MOTOR_PINS)):
            GPIO.output( self.MOTOR_PINS[pin], self.STEP_SEQUENCE[self.motor_step_counter][pin] )


    #Move motor amount of steps with a delay between steps
    def rotate_motor_step_count(self, steps, clock_wise, delay):
        for i in range(steps):
            self.rotate_motor_single_step(clock_wise)
            time.sleep(delay)


    #convert an angle to a step count    
    def convert_angle_to_step_count(angle):
        step_count_full_rotation = 4048
        step_count_quater_rotation =  step_count_full_rotation/4
        percentage = angle / 90
        return int(step_count_quater_rotation * percentage)


    #convert a step count to the an angle
    def convert_step_count_to_angle(step_count):
        step_count_full_rotation = 4048
        step_count_percentage = step_count / step_count_full_rotation
        return 360 * step_count_percentage