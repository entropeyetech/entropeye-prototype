from picamera import PiCamera
import time
import datetime
import telepot
import os
import subprocess
from subprocess import call

bot = telepot.Bot("5642999551:AAHaQMtfSoJ8ipznzq6oyYnosb96Eg4BGfA")
chat_id = "17892141"

camera = PiCamera()
time.sleep(2)
camera.resolution = (1280, 720)
camera.vflip = True
camera.contrast = 10

timestamp = datetime.datetime.now().strftime("%d-%m-%Y_%H:%M:%S")
video_file = "/home/pi/Desktop/EntropEYE-Camera/videocapture/video_{}.h264".format(timestamp)
video_file_mp4 = "/home/pi/Desktop/EntropEYE-Camera/videocapture/video_{}.mp4".format(timestamp)

print("Sto registrando...")
camera.start_recording(video_file)
camera.wait_recording(10)
camera.stop_recording()

subprocess.run(['ffmpeg', '-i', video_file, video_file_mp4])

print("Fatto")

bot.sendMessage(chat_id,'Ti sto inviando un video...')
bot.sendVideo(chat_id, video=open(video_file_mp4, "rb"))