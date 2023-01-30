import time
import datetime
import os
import subprocess
import Adafruit_ADXL345
import RPi.GPIO as GPIO
import telepot

# Imposta il sensore HC-SR04
GPIO.setmode(GPIO.BCM)
GPIO.setup(<TRIG_PIN>, GPIO.OUT)
GPIO.setup(<ECHO_PIN>, GPIO.IN)

# Imposta l'accelerometro ADXL345
accelerometer = Adafruit_ADXL345.ADXL345()

# Imposta il Chatbot BotFather Telegram
bot = telepot.Bot("<BOT_TOKEN>")

def measure_distance():
    # Misura la distanza dal sensore HC-SR04
    GPIO.output(<TRIG_PIN>, True)
    time.sleep(0.00001)
    GPIO.output(<TRIG_PIN>, False)
    start = time.time()

    while GPIO.input(<ECHO_PIN>) == 0:
        start = time.time()

    while GPIO.input(<ECHO_PIN>) == 1:
        stop = time.time()

    elapsed = stop - start
    distance = elapsed * 17150
    return distance

def take_picture_and_video():
    # Crea un timestamp per il file
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    picture_filename = " picture_{}.jpg".format(timestamp)
    video_filename = " video_{}.h264".format(timestamp)

    # Scatta una foto
    os.system("raspistill -o {}".format(picture_filename))

    # Registra un video
    os.system("raspivid -o {} -t 5000".format(video_filename))

    # Converte il video in formato mp4
    mp4_filename = " video_{}.mp4".format(timestamp)
    subprocess.call(["MP4Box", "-add", video_filename, mp4_filename])
    os.remove(video_filename)

    # Invia la foto e il video al Chatbot BotFather Telegram
    with open(picture_filename, "rb") as f:
        bot.sendPhoto(<CHAT_ID>, f)
    with open(mp4_filename, "rb") as f:
        bot.sendVideo(<CHAT_ID>, f)
    os.remove(picture_filename)
    os.remove(mp4_filename)

def main():
    while True:
        # Verifica la distanza dal sensore HC-SR04
        distance = measure_distance()
        if distance < 10:
            # Verifica l'accelerazione dall'accelerometro ADXL345
            x, y, z = accelerometer.read()
            if x > <THRESHOLD> or y > <THRESHOLD> or z > <THRESHOLD>:
                take_ picture_and_video()
        time.sleep(1)

if __name__ == "__main__":
