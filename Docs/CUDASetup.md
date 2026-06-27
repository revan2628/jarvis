# CUDA Setup Guide

This document describes the process of setting up CUDA for Faster-Whisper, the problems encountered, and the final solution used in this project.

---

# Why CUDA?

Jarvis uses **Faster-Whisper** for speech recognition.

Faster-Whisper can run on:

* CPU
* NVIDIA GPU (CUDA)

Running on the GPU significantly reduces transcription time, making the assistant feel much more responsive.

Voice Activity Detection (Silero VAD), however, runs on the CPU because it is lightweight and does not benefit significantly from GPU acceleration.

Current architecture:

```
Silero VAD  --> CPU
Faster-Whisper --> GPU
```

---

# Initial Problem

The first attempt to run Faster-Whisper resulted in an error similar to:

```
Library cublas.so not found
```

This happened because Faster-Whisper depends on NVIDIA CUDA libraries, but they were not installed on the system.

---

# First Attempt

The obvious solution seemed to be installing the CUDA Toolkit.

```
sudo apt install nvidia-cuda-toolkit
```

This downloaded roughly **10 GB** of packages.

Although this solved the missing library problem, it felt excessive since Jarvis only required a few CUDA runtime libraries.

---

# What I Learned

Installing the complete CUDA Toolkit is usually unnecessary if the goal is only to run Faster-Whisper.

The libraries Faster-Whisper primarily depends on are:

* cuBLAS
* cuDNN

Unfortunately, installing only these libraries can be confusing on some Linux distributions, so the full toolkit was used for simplicity.

---

# CPU vs GPU Decision

I considered moving everything to the CPU to avoid CUDA completely.

Advantages:

* Smaller installation
* Simpler dependencies
* Easier setup

Disadvantages:

* Slower transcription
* Higher CPU usage during inference

After testing, I decided on a hybrid approach.

---

# Final Decision

## Faster-Whisper

Runs on the GPU.

Reason:

Speech transcription is computationally expensive, and GPU acceleration makes a noticeable difference in responsiveness.

Model:

```
small
```

Configuration:

```python
WhisperModel(
    "small",
    device="cuda",
    compute_type="float16"
)
```

---

## Silero VAD

Runs on the CPU.

Reason:

VAD processes only tiny audio chunks (~32 ms each).

Its computational cost is extremely low, so using the GPU provides little practical benefit.

PyTorch CPU was installed inside the virtual environment specifically for Silero VAD.

---

# Lessons Learned

## 1. Bigger is not always better

Installing the complete CUDA Toolkit solved the issue, but most of its components are unused by this project.

---

## 2. Read the error carefully

The missing dependency was **not CUDA itself**, but one of its runtime libraries.

Understanding exactly which library is missing saves a lot of unnecessary troubleshooting.

---

## 3. Keep workloads separate

Different components have different computational requirements.

Instead of forcing everything onto the GPU, it is better to assign each task to the hardware best suited for it.

Current pipeline:

```
Microphone
      │
      ▼
Silero VAD (CPU)
      │
      ▼
Speech detected
      │
      ▼
Faster-Whisper (GPU)
      │
      ▼
Text
```

---

# Advice for Future Me

If Jarvis is moved to another computer:

1. Verify that NVIDIA drivers are installed.
2. Check that CUDA runtime libraries are available.
3. Test Faster-Whisper before debugging any speech recognition code.
4. If GPU support becomes too difficult to maintain, switching Whisper to CPU is always an option—the assistant will still work, only with slower transcription.

---

# Final Thoughts

The biggest lesson from this setup was that machine learning projects are often limited more by **dependencies** than by code.

Getting the environment configured correctly took significantly longer than writing the speech recognition pipeline itself.

