## Zoom in/out (fake motion) effect from a static image

A simple python script that creates a fake motion zoom video (.mp4 output) from a static image by zooming in or out on a specified focal point. To run the script:

```
python fakemotion.py <image_path> <output_path> --zoom_in <True/False> --duration <seconds> --fps <fps_value> --focus_x <x> --focus_y <y> --max_zoom <zoom_value>
```

### Example:

```
python fakemotion.py image.jpg zoom_video.mp4 --zoom_in True --duration 5 --fps 30 --focus_x 0.9 --focus_y 0.5 --max_zoom 2
```

Output is a 5 seconds video (30 fps) of zooming (2x) at the point that is roughly middle (y=0.5) right (x=0.9) part of the image.

![Example (converted to .gif)](samples/example_output.gif)

### Requirements/Dependencies:
```bash
pip install opencv-python moviepy numpy argparse
