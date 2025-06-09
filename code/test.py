import cv2
import numpy as np
import time

window_name = "TestWindow"

# Fullscreen dimensions
screen_width = 1920
screen_height = 1080

# Create black frame
black_frame = np.zeros((screen_height, screen_width, 3), dtype=np.uint8)

# Wait a moment to let display initialize
time.sleep(1)

# Create named window
cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

while True:
    cv2.imshow(window_name, black_frame)
    key = cv2.waitKey(1)
    if key == 27:  # ESC
        break

cv2.destroyAllWindows()