from controller_reader import LeftStickXReader 
import time
import subprocess

#used modules
reader = LeftStickXReader()

#gloabal variables
target_angle = 0


#main program ---------------------------------------------------------------------------------
try:
    while True:
        target_angle = reader.get_left_stick_angle()
        print(f"Target Angle: {target_angle}")

except KeyboardInterrupt:
    print("Exiting...")
finally:
    reader.close()