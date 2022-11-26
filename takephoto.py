
   
#!/usr/bin/python3

# Capture a JPEG while still running in the preview mode. When you
# capture to a file, the return value is the metadata for that image.
import sys
sys.path.append("/home/pi/picamera2")
from picamera2 import Picamera2

import time
import libcamera

picam2 = Picamera2()

picam2.rotatation = 90
preview_config = picam2.preview_configuration(main={"size": (320, 240)})
picam2.configure(preview_config)

picam2.start()
time.sleep(2)

metadata = picam2.capture_file("peter.jpg")
print(metadata)

picam2.close()
