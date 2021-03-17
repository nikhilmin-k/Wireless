import socket
import neopixel
import os
import board
import sys
import wave
from pydub import AudioSegment
from pydub.playback import play

pixels = neopixel.NeoPixel(board.D18, 30)
white = [25,25,25]
red = [25, 0, 0]
green = [0,25,0]

for i in range(0, len(pixels)-1):
    pixels[i] = white

#get ip addresses
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
UDP_THIS_IP = s.getsockname()[0]
s.close()
UDP_ESP_IP = sys.argv[1]
UDP_PORT = 4210

sock_out = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_in = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

MESSAGE = b"Hi There!"
sock_out.sendto(MESSAGE, (UDP_ESP_IP, UDP_PORT))

sock_in.bind((UDP_THIS_IP, UDP_PORT))

#Audio Stuff
CHANNELS = 1
swidth = 2
multiplier = 1
spf = wave.open('laugh.wav', 'rb')
fps = spf.getframerate()
signal = spf.readframes(-1)

#wf is the modified wav
wf = wave.open('laughmod.wav', 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(swidth)
wf.setframerate(RATE*multiplier)
wf.writeframes(signal)
wf.close()



isgreen = False
while True:
    data, addr = sock_in.recvfrom(256)
    if(int.from_bytes(data,"big")<15):
        for i in range(0, len(pixels)-1):
            pixels[i] = green
        isgreen = True
        #print("is touching finger\n")
    else:
        if(isgreen==True):
            for i in range(0, len(pixels)-1):
                pixels[i] = red
            isgreen = False
        #print("not touching finger\n")
