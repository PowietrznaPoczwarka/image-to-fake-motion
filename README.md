## Zoom in/out (fake motion) effect from a static image

A simple python script that creates a fake motion zoom video (.mp4 output) from a static image by zooming in or out on a specified focal point. To run the script:

python fakemotion.py <image_path> <output_path> --zoom_in <True/False> --duration <seconds> --fps <fps_value> --focus_x <x> --focus_y <y> --max_zoom <zoom_value>

Requirements/Dependencies:
```bash
pip install opencv-python moviepy numpy argparse
