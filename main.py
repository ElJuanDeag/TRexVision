import cv2
import ffmpeg
import os
import sys
import numpy as np
from tqdm import tqdm


def process_video(input_path: str, output_path: str = "./output.mp4"):
    temp_video = ".temp.avi"

    # open input
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        print(
            "Could not open video! Are you sure the path is correct? Or the file is a valid video?"
        )
        sys.exit(1)

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  # width
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # height
    fps = int(cap.get(cv2.CAP_PROP_FPS))  # fps
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))  # frame count
    fourcc = cv2.VideoWriter_fourcc(*"XVID")  # codec
    out = cv2.VideoWriter(
        temp_video, fourcc, fps, (frame_width, frame_height), isColor=False
    )

    ret, _ = cap.read()
    if not ret:
        print(
            "Could not read the first frame of the file! Are you sure the video isn't corrupted?"
        )
        cap.release()
        sys.exit(2)

    # generate a static black and white noise background
    static_noise = np.random.randint(
        0, 256, (frame_height, frame_width), dtype=np.uint8
    )

    with tqdm(total=total_frames, desc="Processing", unit="frame") as pbar:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            luma_matte = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)[1]
            luma_matte_inv = cv2.bitwise_not(luma_matte)

            # generate a second black and white noise layer for dynamic effect
            dynamic_noise = np.random.randint(
                0, 256, (frame_height, frame_width), dtype=np.uint8
            )

            # apply luma matte over the noise layers
            masked_static_noise = cv2.bitwise_and(
                static_noise, static_noise, mask=luma_matte_inv
            )
            masked_dynamic_noise = cv2.bitwise_and(
                dynamic_noise, dynamic_noise, mask=luma_matte
            )

            result = cv2.add(masked_static_noise, masked_dynamic_noise)

            out.write(result)
            pbar.update(1)

    cap.release()
    out.release()

    print("Merging audio...")
    # extract and merge audio
    video_stream = ffmpeg.input(temp_video)
    audio_stream = ffmpeg.input(input_path)
    ffmpeg.output(
        video_stream["v:0"],
        audio_stream["a:0"],
        output_path,
    ).run(overwrite_output=True)

    os.remove(temp_video)
    print(f"Saved as {output_path}!")

    input("Press enter to exit.")


if len(sys.argv) < 2:
    print(
        "To use this program, please provide a video path as an argument. For example, if you're running from the command line, it would be `py main.py video.mp4` (or something like that)."
    )
    if sys.platform == "win32":
        # this message will only appear on windows
        # if you're on linux or mac pylance (vscode) will say that this code is unreachable, just ignore it
        print(
            "Note that you can also drag and drop a video onto the file in your file explorer without using the command line."
        )
else:
    process_video(sys.argv[1])
