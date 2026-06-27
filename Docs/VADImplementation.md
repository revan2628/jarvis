#Implementing VAD

At first I wanted to use threshold values to understand if the user is speaking, but when i considered background noises I quickly understood the need for a VAD

I've implemented a state machine containing 2 states, either LISTENING or RECORDING
- if the state is listening and no speech is detected, it keeps listening
- if the state is listening and speech is detected, it changes the state to RECORDING and clears the audio chunks (numpy arrays of silence) and starts recording speech
- if the state is recording and speech is detected, we keep recording
- if the state is recording and no speech is detected, a variable called silent_chunks increases by 1 for every consecutive silent chunk encountered. If the number of silent chunks reaches a set threshold, we stop recording and set the
state to LISTENING
- the chunks saved are then concatenated and sent to whisper for transcription

problems faced:
- the biggest problem ive faced was that VAD takes around 5-6 chunks (at 512 blocksize and 16KHz samplerate) to detect speech and start recording, leading to clipped audio, so i had to implement a preroll buffer to keep track of the previous 7-8 chunks and append these to the list
- To implement a preroll buffer I've used a deque of maximum length=8 (around 384ms)
