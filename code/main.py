from controller_reader import Controller_Reader 
from animationdriver import AnimationPlayer
import time
COLORS = ["Blue", "Green", "Red", "Turquise"]
x_button_pressed_last_frame = False

#used modules
controller = Controller_Reader()
animationPlayer = AnimationPlayer(200, 0.8)
#gloabal variables
last_animation_type = "Straight"
last_animation_color = "Red"

#Functions ---------------------------------------------------------------------------------
def change_animation_type():
    global last_animation_type
    
    current_angle = controller.get_left_stick_angle()
    target_animation_type = get_animation_type(current_angle)
    if target_animation_type != last_animation_type:
        animationPlayer.change_animation_type(target_animation_type)
    
    last_animation_type = target_animation_type



def change_animation_color():
    global last_animation_color, x_button_pressed_last_frame
    
    current_pressed = controller.is_x_button_pressed() == 1

    # Detect rising edge (button just pressed)
    if current_pressed and not x_button_pressed_last_frame:
        # increase color by one
        index_current_color = COLORS.index(last_animation_color)
        index_next_color = (index_current_color + 1) % len(COLORS)
        last_animation_color = COLORS[index_next_color]
        animationPlayer.change_animation_color(last_animation_color)

    # Update the last frame pressed state
    x_button_pressed_last_frame = current_pressed
def get_animation_type(angle):
    if angle < -54:
        return "Sharp_Left"
    if angle >=-54 and angle < -18:
        return "Medium_Left"
    if angle >= -18 and angle <= 18:
        return "Straight"
    if angle >18 and angle <= 54:
        return "Medium_Right"
    if angle > 54 :
        return "Sharp_Right"
#main program ---------------------------------------------------------------------------------
try:
    while True:
        change_animation_color()
        change_animation_type()
        print(f"Animation Type: {last_animation_type}   Animation Color: {last_animation_color}")
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Exiting...")
finally:
    controller.close()
    animationPlayer.stop()