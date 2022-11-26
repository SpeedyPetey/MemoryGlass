print("importing...", end='', flush=True)

import sys
import pyttsx3
sys.path.append("/home/pi/picamera2")
from picamera2 import Picamera2
import numpy as np
import os
import cv2
import RPi.GPIO as GPIO
import face_recognition
print("done")

DISPLAYCAM = False
try:
    for i in range(len(sys.argv)):
        if sys.argv[i] == '--cameraon' or sys.argv[i] == '--co':
            DISPLAYCAM = True
except Exception as e:
    pass
print("setting up button...", end='', flush=True)
GPIO.setmode(GPIO.BCM)
GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_UP)
print("done")

print("setting up voice...", end='', flush=True)
engine = pyttsx3.init()
print("done")

if DISPLAYCAM:
    cv2.startWindowThread()
print("setting up camera...", end='', flush=True)
picam2 = Picamera2()
preview_config = picam2.preview_configuration(lores={"size": (640, 480)})
picam2.configure(preview_config)
picam2.start()
print("done\n")

# Load a sample picture and learn how to recognize it.
print("Loading known face image(s)...", end='', flush=True)


# Initialize some variables
face_locations = []
face_encodings = []
face_names = []

#new variables
known_person=[]
known_image=[]
known_face_encoding=[]

#Loop to add images in friends folder
for file in os.listdir("friends/pics"):
    try:
        #Extracting person name from the image filename eg: david.jpg
        known_person.append(file.replace(".jpg", ""))
        file=os.path.join("friends/pics", file)
        known_image = face_recognition.load_image_file(file)
        known_face_encoding.append(face_recognition.face_encodings(known_image)[0])
    except Exception as e:
        pass
print("done")

while True:
    if DISPLAYCAM:
        
        output = picam2.capture_array("lores")
        rgb = cv2.cvtColor(output, cv2.COLOR_YUV420p2RGB)
        rgbproper = cv2.rotate(rgb, cv2.ROTATE_90_CLOCKWISE)
        cv2.imshow("Camera", rgbproper)
        
    if (not GPIO.input(5)):
        print("Capturing image...", end="", flush=True)
        # Grab a single frame of video from the RPi camera as a numpy array
        output = picam2.capture_array("lores")
        rgb = cv2.cvtColor(output, cv2.COLOR_YUV420p2RGB)
        rgbproper = cv2.rotate(rgb, cv2.ROTATE_90_CLOCKWISE)
        cv2.imshow("Camera", rgbproper)

        print("done")
    
        print("Finding faces...", end="", flush=True)
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgbproper)
        print("done")
        print("Found {} faces in image.".format(len(face_locations)))
        face_encodings = face_recognition.face_encodings(rgbproper, face_locations)
        name = ""
        # Loop over each face found in the frame to see if it's someone we know.
        for face_encoding in face_encodings:
            match = face_recognition.compare_faces(known_face_encoding, face_encoding)
            matches=np.where(match)[0] #Checking which image is matched
            if len(matches)>0:
                name = str(known_person[matches[0]])
            else:
                name = "None"
        if name == "":
            pass
        elif name == "None":
            print("no such person exists")
        else:
            print("I see someone named {}!".format(name))
            infofile=os.path.join("friends/info/", name + ".txt")
            engine.say(name)
            engine.runAndWait()
            try:
                with open(infofile) as f:
                    lines = f.read()
                    engine.say(lines)
                    engine.runAndWait()
                    #engine.stop()
                    print(lines)
            except Exception as e:
                pass   
GPIO.cleanup()
