FOLDER_PATH = r"C:\Users\sebas\Desktop\Projektstudium\Code\Projektstudium\animations\full_resolution"
FOLDER_RESULT = r"C:\Users\sebas\Desktop\Projektstudium\Code\Projektstudium\animations\quater_resolution"
import os
import cv2

def resize_video(input_path, output_path, target_width, target_height):
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        print(f"Failed to open {input_path}")
        return
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # codec for .mp4
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    out = cv2.VideoWriter(output_path, fourcc, fps, (target_width, target_height))
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        resized_frame = cv2.resize(frame, (target_width, target_height))
        out.write(resized_frame)
    
    cap.release()
    out.release()
    print(f"Saved resized video to {output_path}")

def resize_clips_in_folder(source_folder, output_folder, target_width, target_height):
    for root, dirs, files in os.walk(source_folder):
        # Compute relative path to preserve folder structure
        rel_path = os.path.relpath(root, source_folder)
        output_subfolder = os.path.join(output_folder, rel_path)
        os.makedirs(output_subfolder, exist_ok=True)

        for file in files:
            if file.lower().endswith(".mp4"):
                input_file_path = os.path.join(root, file)
                output_file_path = os.path.join(output_subfolder, file)

                resize_video(input_file_path, output_file_path, target_width, target_height)

source_folder = FOLDER_PATH
output_folder = FOLDER_RESULT
target_width = int(250)
target_height = int(250)

resize_clips_in_folder(source_folder, output_folder, target_width, target_height)
