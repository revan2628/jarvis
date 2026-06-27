import sounddevice as sd
from faster_whisper import WhisperModel

model_size = 'small'
model = WhisperModel(model_size, device='cuda', compute_type='float16')
def fwtransc(utterance):
    segments, info = model.transcribe(utterance, beam_size=2, language='en')
    full_text = " ".join([segment.text for segment in segments])
    return full_text
