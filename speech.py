from piper.voice import PiperVoice
import subprocess
import time
import wave
import os

voice = PiperVoice.load("/home/revan/Documents/Robotics/Jarvis/voices/joe/en_US-joe-medium.onnx")
def speak(text):
    with wave.open("output.wav", "wb") as wav_file:
        voice.synthesize_wav(text, wav_file)
    subprocess.run(["aplay", "output.wav"], check=True)
    os.remove("output.wav")


