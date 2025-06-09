import pygame
import time

class Controller_Reader:
    def __init__(self, controller_index=0):
        start_pigpiod()
        pygame.init()
        controller_connected = False

        while not controller_connected:
            pygame.joystick.quit()  # Reset joystick subsystem
            pygame.joystick.init()  # Reinitialize it

            if pygame.joystick.get_count() == 0:
                print("No Controller Connected")
                time.sleep(0.5)
                continue

            self.joystick = pygame.joystick.Joystick(controller_index)
            self.joystick.init()
            controller_connected = True

        print(f"Initialized controller: {self.joystick.get_name()}")


    def get_left_stick_x(self):
        pygame.event.pump()  # Updates joystick events
        x_axis = self.joystick.get_axis(0)  # Axis 0 is typically left stick X
        return min(1,max(-1,x_axis))
    

    def get_left_stick_angle(self):
        value = self.get_left_stick_x()
        return value * 90

    def is_x_button_pressed(self):
        pygame.event.pump()  # Update joystick events
        return self.joystick.get_button(2) == 1
    
    def close(self):
        pygame.joystick.quit()
        pygame.quit()


import subprocess

def start_pigpiod():
    # Check if pigpiod is running
    result = subprocess.run(['pgrep', 'pigpiod'], capture_output=True, text=True)
    if result.returncode != 0:
        # pigpiod not running, so start it
        print("Starting pigpiod daemon...")
        subprocess.run(['sudo', 'systemctl', 'start', 'pigpiod'])
    else:
        print("pigpiod daemon already running.")
