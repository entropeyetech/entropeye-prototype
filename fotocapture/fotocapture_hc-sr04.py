from picamera import PiCamera
import time
import datetime
import RPi.GPIO as GPIO
import telepot

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.IN)
GPIO.setwarnings(False)

camera = PiCamera()
time.sleep(2)
camera.resolution = (1920, 1080)
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
        picture_filename = "/home/pi/Desktop/EntropEYE-Camera/fotocapture/image_{}.jpg".format(timestamp)

        print("Sto scattando...")
        camera.capture(picture_filename)

        print("Fatto")

        bot.sendMessage(chat_id,'Ti sto inviando una foto...')
        bot.sendPhoto(chat_id, photo=open(picture_filename, 'rb'))

   time.sleep(1)

GPIO.cleanup()
