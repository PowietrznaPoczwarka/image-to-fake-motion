import cv2
from moviepy.editor import ImageSequenceClip
import argparse

import numpy as np

def log_scale(t):
    # Logarithmic scale function to smoothen the zoom that would otherwise accelaret near the end.
    return np.log(1 + t * (np.e - 1))

def create_zoom_video(image_path, output_path="fakemotion_video.mp4", zoom=True, duration=10, fps=30, focus_point={"x": 0.5, "y": 0.5}, max_zoom=1.5):
    try:
        image = cv2.imread(image_path)
        height, width, color_channels = image.shape
        n_frames = duration * fps
        frames = []

        # calculate the final frame size and starting points
        # final frame size
        min_width = int(width / max_zoom)
        min_height = int(height / max_zoom)

        # starting point of the final frame (n)
        start_n_x = min(max(0, int(width * focus_point["x"]) - min_width // 2), width - min_width)
        start_n_y = min(max(0, int(height * focus_point["y"]) - min_height // 2), height - min_height)

        # ending point of the final frame (n)
        end_n_x = start_n_x + min_width
        end_n_y = start_n_y + min_height

        # linspace and logarithmic scaling
        t_values = np.linspace(0, 1, n_frames)
        log_t_values = log_scale(t_values)

        # log-scaled interpolation
        start_x_range = (1 - log_t_values) * 0 + log_t_values * start_n_x
        start_y_range = (1 - log_t_values) * 0 + log_t_values * start_n_y
        end_x_range = (1 - log_t_values) * width + log_t_values * end_n_x
        end_y_range = (1 - log_t_values) * height + log_t_values * end_n_y

        # zoom_range = np.linspace(1, max_zoom, n_frames) if zoom else np.linspace(max_zoom, 1, n_frames)

        for i in range(n_frames):
            zoomed_img = cv2.resize(
                image[int(start_y_range[i]):int(end_y_range[i]), int(start_x_range[i]):int(end_x_range[i])],
                (width, height)
            )
            frames.append(zoomed_img)

        video = ImageSequenceClip([cv2.cvtColor(f, cv2.COLOR_BGR2RGB) for f in frames], fps=fps)
        video.write_videofile(output_path, codec='libx264')

        return True

    except Exception as e:
        print(e)
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a fake motion zoom video from an image.")
    
    parser.add_argument('image_path', type=str, help="Path to the input image.")
    parser.add_argument('output_path', type=str, help="Path to the output video file (e.g., output.mp4).")
    parser.add_argument('--zoom_in', type=bool, default=True, help="Whether to zoom in or zoom out.")
    parser.add_argument('--duration', type=int, default=10, help="Duration of the video in seconds.")
    parser.add_argument('--fps', type=int, default=30, help="Frames per second for the video.")
    parser.add_argument('--focus_x', type=float, default=0.5, help="X-coordinate for the focus point (value between 0 and 1).")
    parser.add_argument('--focus_y', type=float, default=0.5, help="Y-coordinate for the focus point (value between 0 and 1).")
    parser.add_argument('--max_zoom', type=float, default=1.5, help="Maximum zoom level.")

    args = parser.parse_args()

    focus_point = {"x": args.focus_x, "y": args.focus_y}

    create_zoom_video(
        image_path=args.image_path,
        output_path=args.output_path,
        zoom=args.zoom_in,
        duration=args.duration,
        fps=args.fps,
        focus_point=focus_point,
        max_zoom=args.max_zoom
    )
