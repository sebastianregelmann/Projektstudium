import pygame

class LeftStickXReader:
    def __init__(self, controller_index=0):
        pygame.init()
        pygame.joystick.init()
        
        if pygame.joystick.get_count() == 0:
            raise Exception("No joystick/controller connected")
        
        self.joystick = pygame.joystick.Joystick(controller_index)
        self.joystick.init()
        print(f"Initialized controller: {self.joystick.get_name()}")


    def get_left_stick_x(self):
        pygame.event.pump()  # Updates joystick events
        x_axis = self.joystick.get_axis(0)  # Axis 0 is typically left stick X
        return min(1,max(-1,x_axis))
    

    def get_left_stick_angle(self):
        value = self.get_left_stick_x()
        return value * 90


    def close(self):
        pygame.joystick.quit()
        pygame.quit()


