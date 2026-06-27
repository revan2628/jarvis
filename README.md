# Jarvis

A modular voice assistant for Linux inspired by Iron Man's J.A.R.V.I.S.

This project started as a simple Python automation assistant and has gradually evolved into a real-time voice assistant capable of listening continuously, detecting speech, transcribing commands locally, and executing them.

Unlike many assistant projects, this repository focuses heavily on understanding the engineering behind speech recognition rather than simply using existing libraries.

---

## Current Features

- 🎙️ Real-time speech recognition
- 🧠 Silero Voice Activity Detection (VAD)
- ⚡ Faster-Whisper transcription (GPU accelerated)
- 🗣️ Offline text-to-speech using Piper
- 📺 Open and search YouTube
- 📂 Find and open files and folders
- 📝 Voice-controlled todo list
- 🔒 Lock the computer
- 💻 Open Jarvis source code
- Modular command handler architecture

---

## Tech Stack

- Python
- Faster-Whisper
- Silero VAD
- PyTorch (CPU)
- Piper TTS
- SoundDevice
- NumPy

---

## Architecture

Microphone
↓
Silero Voice Activity Detection
↓
Audio Buffer
↓
Faster-Whisper
↓
Command Handlers

---

## Project Goals

The long-term goal is to build a desktop AI assistant that can:

- Understand natural language
- Control the operating system
- Manage files
- Automate repetitive tasks
- Integrate with local LLMs
- Eventually become the software brain for future robotics projects

---

## Lessons Learned

This project taught me much more than Python syntax.

Some of the topics explored include:

- Streaming audio
- Voice Activity Detection
- State machines
- Whisper inference
- CPU vs GPU inference
- Audio preprocessing
- Software architecture
- Modular design
- Linux automation

A detailed engineering journal can be found inside the `docs/` folder.

---

## Current Status

This project is actively being developed.

Many more commands and AI capabilities are planned.
