import cv2
import numpy as np
from moviepy.editor import ImageSequenceClip
import argparse

def create_zoom_video(image_path, output_path, zoom_in=True, duration=5, fps=30, focus_point={"x": 0.5, "y": 0.5}, max_zoom=1.5):
    image = cv2.imread(image_path)
    
    if image is None:
        print("Error: Could not load image.")
        return False

    h, w, _ = image.shape
    num_frames = duration * fps

    frames = []

    # Either zoming in (zoom == True) or zooming out (zoom == False)
    zoom_range = np.linspace(1, max_zoom, num_frames) if zoom_in else np.linspace(max_zoom, 1, num_frames)

    focus_x = int(w * focus_point['x'])
    focus_y = int(h * focus_point['y'])

    for zoom_factor in zoom_range:
        new_w = int(w / zoom_factor)
        new_h = int(h / zoom_factor)

        start_x = max(0, min(focus_x - new_w // 2, w - new_w))
        start_y = max(0, min(focus_y - new_h // 2, h - new_h))

        zoomed_img = image[start_y:start_y + new_h, start_x:start_x + new_w]
        zoomed_img = cv2.resize(zoomed_img, (w, h))

        frames.append(zoomed_img)

    # Convert frames to a video using MoviePy
    clip = ImageSequenceClip([cv2.cvtColor(f, cv2.COLOR_BGR2RGB) for f in frames], fps=fps)

    # Export as mp4
    clip.write_videofile(output_path, codec='libx264')

    print("Video created successfully!")
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a fake motion zoom video from an image.")
    parser.add_argument('image_path', type=str, help='Path to the input image.')
    parser.add_argument('output_path', type=str, help='Path to the output video file (e.g., output.mp4).')
    parser.add_argument('--zoom_in', type=bool, default=True, help='Whether to zoom in or out. Default is True (zoom in).')
    parser.add_argument('--duration', type=int, default=5, help='Duration of the video in seconds. Default is 5.')
    parser.add_argument('--fps', type=int, default=30, help='Frames per second for the video. Default is 30.')
    parser.add_argument('--focus_x', type=float, default=0.5, help='X-coordinate for the focus point (0 to 1). Default is 0.5.')
    parser.add_argument('--focus_y', type=float, default=0.5, help='Y-coordinate for the focus point (0 to 1). Default is 0.5.')
    parser.add_argument('--max_zoom', type=float, default=1.5, help='Maximum zoom level. Default is 1.5.')

    args = parser.parse_args()

    focus_point = {"x": args.focus_x, "y": args.focus_y}
    create_zoom_video(args.image_path, args.output_path, zoom_in=args.zoom_in, duration=args.duration, fps=args.fps, focus_point=focus_point, max_zoom=args.max_zoom)
