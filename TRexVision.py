import cv2
import numpy as np
import os
from tqdm import tqdm
import subprocess

def process_video(input_path, output_path):
    temp_video = "temp_video.avi"
    
    # Open the input video
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return
    
    # Get video properties
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(temp_video, fourcc, fps, (frame_width, frame_height), isColor=False)
    
    ret, prev_frame = cap.read()
    if not ret:
        print("Error: Could not read first frame.")
        cap.release()
        return
    
    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
    
    # Create a static black and white noise background
    static_noise = np.random.randint(0, 256, (frame_height, frame_width), dtype=np.uint8)
    
    # Initialize progress bar
    with tqdm(total=total_frames, desc="Processing Video", unit="frame") as pbar:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            luma_matte = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)[1]
            luma_matte_inv = cv2.bitwise_not(luma_matte)
            
            # Generate a second black and white noise layer for dynamic effect
            dynamic_noise = np.random.randint(0, 256, (frame_height, frame_width), dtype=np.uint8)
            
            # Apply luma matte over the noise layers
            masked_static_noise = cv2.bitwise_and(static_noise, static_noise, mask=luma_matte_inv)
            masked_dynamic_noise = cv2.bitwise_and(dynamic_noise, dynamic_noise, mask=luma_matte)
            
            result = cv2.add(masked_static_noise, masked_dynamic_noise)
            
            out.write(result)
            prev_gray = gray.copy()
            pbar.update(1)  # Update progress bar
    
    cap.release()
    out.release()
    
    print("Merging audio...")
    # Use ffmpeg to extract and merge audio
    ffmpeg_cmd = [
        "ffmpeg", "-y", "-i", temp_video, "-i", input_path, "-c:v", "copy", "-c:a", "aac", "-strict", "experimental", "-map", "0:v:0", "-map", "1:a:0", output_path
    ]
    subprocess.run(ffmpeg_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Delete temporary video file
    os.remove(temp_video)
    print(f"Processed video with audio saved as {output_path}")

# Example usage
root_path = os.path.dirname(os.path.abspath(__file__)).replace('\\','/')
inputPath=root_path+'/inputFiles/'
outputPath=root_path+'/outputFiles/'
process_video(inputPath+'BadApple.mp4', outputPath+'output_staticLumaMatteAudio.avi')
