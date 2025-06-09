#!/usr/bin/python3
import pigpio
import time



class Servo:
    def __init__(self, controller_index=0): 
        self.SERVO_PIN = 23
        self.pi = pigpio.pi()
        if not self.pi.connected:
            try:
                # Check if pigpiod is already running, otherwise start it
                subprocess.run(["sudo", "pigpiod"], check=True)
                print("pigpiod started successfully.")
                self.pi = pigpio.pi()
            except subprocess.CalledProcessError as e:
                print(f"Error starting pigpiod: {e}")
    
    #set servo motor to a angle
    def set_servo(self, angle):
        pulse = self.angle_to_pulse(angle)
        self.pi.set_servo_pulsewidth(self.SERVO_PIN, pulse)

    
    def angle_to_pulse(self, angle):
        angle += 90
        # Clamp angle between 0 and 180
        angle = max(0, min(180, angle))
        #flip angle to match controller
        angle = 180- angle
        pulsewidth = 500 + (angle / 180.0) * 2000  # 500 to 2500 µs
        return pulsewidth