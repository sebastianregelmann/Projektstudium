import cv2
import numpy as np
import time
import threading
from pathlib import Path


class AnimationPlayer:
    def __init__(self, animation_delay=500, playback_speed=1):
        self.current_dir = Path(__file__).resolve().parent
        self.FOLDERNAMES = ["Medium_Left", "Medium_Right", "Sharp_Left", "Sharp_Right", "Straight"]
        self.COLORS = ["Blue", "Green", "Red", "Turquise"]
        self.PATH = self.current_dir.parent / "animations"/"quater_resolution"
        self.FOLDERPATHS = [self.PATH / folder_name for folder_name in self.FOLDERNAMES]
        self.FRAMETIME = 41.6666
        self.WINDOWNAME = "Animation"

        self.ANIMATION_DELAY = animation_delay
        self.PLAYBACKSPEED = playback_speed

        self.ANIMATIONS = {}
        self.animation_type = "Straight"
        self.animation_color = "Red"
        self.stop_thread = False

        self.BLACKFRAME = None
        self.FRAME_SHAPE = None
        
        #scale properties
        self.SCREEN_WIDTH = 1920
        self.SCREEN_HEIGHT = 1080
        self.SCREEN_RES = (self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        #borderless fullscreen
        # <<< FULLSCREEN FIX START >>>
        time.sleep(1)  # <<< ADDED: Let display initialize
        cv2.namedWindow(self.WINDOWNAME, cv2.WND_PROP_FULLSCREEN)  # <<< CHANGED: Moved after delay
        cv2.setWindowProperty(self.WINDOWNAME, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)  # <<< CHANGED
        # <<< FULLSCREEN FIX END >>>
        
        print("Start Loading Animations")
        self.load_animations()
        print("Animations loaded")

        self.get_frame_shape()
        self.get_black_frame()
        
        print("Start Animation")
        self.anim_thread = threading.Thread(target=self.animation_loop)
        self.anim_thread.start()

    def load_animations(self):
        for folder_path, folder_name in zip(self.FOLDERPATHS, self.FOLDERNAMES):
            color_animations = {}
            for color in self.COLORS:
                video_path = folder_path / f"{color}.mp4"
                cap = cv2.VideoCapture(str(video_path))
                frames = []
                while True:
                    ret, frame = cap.read()
                    if not ret:
                        break
                    frames.append(frame)
                cap.release()
                color_animations[color] = frames
                print("Loaded" + str(color) + str(folder_name))
            self.ANIMATIONS[folder_name] = color_animations

    def get_frame_shape(self):
        animation = self.ANIMATIONS["Straight"]["Red"]
        self.FRAME_SHAPE = animation[0].shape

    def get_black_frame(self):
        self.BLACKFRAME = np.zeros(self.FRAME_SHAPE, dtype=np.uint8)

    def wait_animation(self):
        black_scaled = cv2.resize(self.BLACKFRAME, self.SCREEN_RES, interpolation=cv2.INTER_LINEAR)
        cv2.imshow(self.WINDOWNAME, black_scaled)
        cv2.waitKey(self.ANIMATION_DELAY)

    def animation_loop(self):
        current_type = self.animation_type
        current_color = self.animation_color
        current_animation = self.ANIMATIONS[current_type][current_color]
        frame_index = 0

        while not self.stop_thread:
            if current_type != self.animation_type or current_color != self.animation_color:
                frame_index = 0
                current_type = self.animation_type
                current_color = self.animation_color
                current_animation = self.ANIMATIONS[current_type][current_color]

            if frame_index >= len(current_animation):
                frame_index = 0
                self.wait_animation()

            start_time = time.time()
            frame = current_animation[frame_index]
            frame_scaled = cv2.resize(frame, self.SCREEN_RES, interpolation=cv2.INTER_LINEAR)
            cv2.imshow(self.WINDOWNAME, frame_scaled)
            end_time = time.time()
            delay_ms = max(1, int(self.FRAMETIME / self.PLAYBACKSPEED - (end_time - start_time) * 1000))

            if cv2.waitKey(delay_ms) == 27:  # ESC to exit
                self.stop_thread = True
                break

            frame_index += 1

    def change_animation_color(self, new_color):
        self.animation_color = new_color

    def change_animation_type(self, new_type):
        self.animation_type = new_type

    def animation_test(self):
        animation_loops = 2
        for anim_type in self.FOLDERNAMES:
            for color in self.COLORS:
                self.change_animation_type(anim_type)
                self.change_color(color)
                animation_length = len(self.ANIMATIONS[anim_type][color])
                time_per_loop = (animation_length * self.FRAMETIME) / 1000
                time.sleep(animation_loops * time_per_loop + animation_loops * (self.ANIMATION_DELAY / 1000))

    def stop(self):
        self.stop_thread = True
        self.anim_thread.join()
        cv2.destroyAllWindows()