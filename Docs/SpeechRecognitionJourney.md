# Building Speech Recognition

Initially I recorded fixed-length audio using sounddevice.rec().

Problems:

- Required speaking within a fixed time
- Wasted computation on silence
- Poor user experience

I then learned about streaming audio using InputStream.

Next I explored Voice Activity Detection.

Instead of relying on amplitude thresholds, I implemented Silero VAD, allowing Jarvis to distinguish human speech from background sounds.

Finally I connected the speech pipeline to Faster-Whisper, creating a continuous speech interface.
