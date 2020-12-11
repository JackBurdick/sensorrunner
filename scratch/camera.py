import time

from picamera import PiCamera

"""

will be revisiting at a later date

"""

# comments: https://www.raspberrypi.org/forums/viewtopic.php?f=43&t=50142&start=25
# adapter: https://github.com/ArduCAM/RaspberryPi/tree/master/Multi_Camera_Adapter/Multi_Adapter_Board_4Channel/Multi_Camera_Adapter_V2.1_python
# picamera: https://github.com/waveform80/picamera/blob/master/picamera/camera.py
# raspistill -o/home/pi/dev/imgs/example_c.jpg

if __name__ == "__main__":
    out_path = "/home/pi/dev/imgs/example_a.jpg"
    # 2592 x 1944
    camera = PiCamera(resolution=(2592, 1944), framerate=30)
    # # Set ISO to the desired value
    # camera.iso = 100
    # # Wait for the automatic gain control to settle
    # time.sleep(2)
    # # Now fix the values
    # camera.shutter_speed = camera.exposure_speed
    # camera.exposure_mode = "off"
    # g = camera.awb_gains
    # camera.awb_mode = "off"
    # camera.awb_gains = g
    # time.sleep(2)
    camera.capture(out_path)
    print(f"image saved? : {out_path}")
