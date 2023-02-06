from picamera import PiCamera
import time
import datetime
import telepot
import os
import subprocess
import RPi.GPIO as GPIO
from subprocess import call

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.IN)
GPIO.setwarnings(False)

camera = PiCamera()
time.sleep(2)
camera.resolution = (1280, 720)
camera.vflip = True
camera.contrast = 10

bot = telepot.Bot("5642999551:AAHaQMtfSoJ8ipznzq6oyYnosb96Eg4BGfA")
chat_id = "17892141"

def measure_distance():
    # Misura la distanza dal sensore HC-SR04
    GPIO.output(23, True)
    time.sleep(0.00001)
    GPIO.output(23, False)
    start = time.time()

    while GPIO.input(24) == 0:
        start = time.time()

    while GPIO.input(24) == 1:
        stop = time.time()

    elapsed = stop - start
    distance = elapsed * 17150
    return distance

while True:
   distance = measure_distance()
   if distance < 10:


        timestamp = datetime.datetime.now().strftime("%d-%m-%Y_%H:%M:%S")
        video_file = "/home/pi/Desktop/EntropEYE-Camera/videocapture/video_{}.h264".format(timestamp)
        video_file_mp4 = "/home/pi/Desktop/EntropEYE-Camera/videocapture/video_{}.mp4".format(timestamp)

        print("Sto registrando...")
        camera.start_recording(video_file)
        camera.wait_recording(2)
        camera.stop_recording()

       subprocess.run(['ffmpeg', '-i', video_file, video_file_mp4])

        print("Fatto")

        bot.sendMessage(chat_id,'Ti sto inviando un video...')
        bot.sendVideo(chat_id, video=open(video_file_mp4, "rb"))

   time.sleep(1)

GPIO.cleanup()