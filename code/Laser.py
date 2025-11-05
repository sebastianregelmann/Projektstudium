#!/usr/bin/python3
import time
import subprocess
import pigpio
import pygame
import sys
import os


PIN_SERVO = 23
PIN_LED_LEFT = 17
PIN_LED_RIGHT = 27

# ------------------------------------------------------------
# Helper Functions
# ------------------------------------------------------------

def ensure_pigpiod_running():
    """Ensure the pigpiod daemon is running."""
    try:
        subprocess.run(["pgrep", "pigpiod"], check=True, stdout=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        print("Starting pigpiod service...")
        subprocess.run(["sudo", "pigpiod"], check=True)
        time.sleep(1)
    print("pigpiod is running.")

# ------------------------------------------------------------
# Servo Driver
# ------------------------------------------------------------

class Servo:
    def __init__(self, pin=23):
        ensure_pigpiod_running()
        self.SERVO_PIN = pin
        self.pi = pigpio.pi()
        if not self.pi.connected:
            raise Exception("Failed to connect to pigpiod.")

    def set_servo(self, angle):
        pulse = self.angle_to_pulse(angle)
        self.pi.set_servo_pulsewidth(self.SERVO_PIN, pulse)

    def angle_to_pulse(self, angle):
        angle += 90
        angle = max(0, min(180, angle))
        angle = 180 - angle
        pulsewidth = 500 + (angle / 180.0) * 2000
        return pulsewidth

# ------------------------------------------------------------
# Controller Reader
# ------------------------------------------------------------

class LeftStickXReader:
    def __init__(self):
        pygame.init()
        pygame.joystick.init()
        self.joystick = None
        self.connect_controller()

    def connect_controller(self):
        """Try to connect to the first available controller."""
        while True:
            pygame.joystick.quit()
            pygame.joystick.init()
            if pygame.joystick.get_count() > 0:
                self.joystick = pygame.joystick.Joystick(0)
                self.joystick.init()
                print(f"Controller connected: {self.joystick.get_name()}")
                return
            else:
                print("No controller detected. Waiting for connection...")
                time.sleep(2)

    def get_left_stick_x(self):
        """Get X-axis value (-1 to 1)."""
        pygame.event.pump()
        if not self.joystick:
            self.connect_controller()
        try:
            x_axis = self.joystick.get_axis(0)
            return min(1, max(-1, x_axis))
        except pygame.error:
            print("Controller disconnected.")
            self.connect_controller()
            return 0

    def get_left_stick_angle(self):
        return self.get_left_stick_x() * 90

    def close(self):
        if self.joystick:
            self.joystick.quit()
        pygame.quit()

# ------------------------------------------------------------
# Main Program
# ------------------------------------------------------------

def main():
    print("Initializing system...")
    servo = Servo(pin=PIN_SERVO)
    reader = LeftStickXReader()
    
    #enable LASER 
    servo.pi.set_mode(PIN_LED_LEFT, pigpio.OUTPUT)
    servo.pi.set_mode(PIN_LED_RIGHT, pigpio.OUTPUT)
    servo.pi.write(PIN_LED_LEFT, 1)
    servo.pi.write(PIN_LED_RIGHT,1)

    current_angle = 0

    print("System ready. Use the left stick to move the servo.")
    print("Press Ctrl+C to exit.")

    try:
        while True:
            target_angle = reader.get_left_stick_angle()
            servo.set_servo(target_angle)
            print(f"Target Angle: {target_angle:.2f}")
            time.sleep(0.05)
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        reader.close()
        print("Clean shutdown complete.")

# ------------------------------------------------------------
# Run
# ------------------------------------------------------------
if __name__ == "__main__":
    main()
