# Jarvis Architecture

Microphone

↓

InputStream

↓

Audio Chunks (32 ms)

↓

Silero VAD

↓

Recording State Machine

↓

Whisper

↓

Command Execution

The speech pipeline has been designed so each module has a single responsibility.

vad.py
Responsible only for detecting complete utterances.

transcription.py
Responsible only for converting speech to text.

jarvis.py
Responsible only for understanding and executing commands.
