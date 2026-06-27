import sounddevice as sd
import torch
from silero_vad import load_silero_vad
import numpy as np
import transcription
from collections import deque

model = load_silero_vad()
def listen():
    history = deque(maxlen=8)
    recording = False
    chunks = []
    silent_chunks = 0

    with sd.InputStream(samplerate=16000,
                        channels=1,
                        dtype='float32',
                        blocksize=512
                        ) as stream:
        print("ctrl+c to stop")
        print("listening...")
        while True:
            audio, overflow = stream.read(512)
            audio = audio.flatten()
            tensor = torch.from_numpy(audio)
            history.append(audio)
            confidence = model(tensor, 16000)
            if not recording:
                if confidence.item() > 0.5:
                    print("Start Recording")
                    recording = True
                    chunks.append(audio)
                    silent_chunks = 0
            else:
                chunks.append(audio)

                if confidence.item()>0.25:
                    silent_chunks = 0
                else:
                    silent_chunks += 1
                if silent_chunks >= 12:
                    print('Recording ended')
                    full_audio = np.concatenate(chunks)
                    full_audio = full_audio.flatten()
                    utterance = transcription.fwtransc(full_audio)
                    recording = False
                    chunks = list(history)
                    silent_chunks = 0
                    return utterance
    return None

