import asyncio
import numpy as np
import torch
from faster_whisper import WhisperModel

# Silero VAD parameters
VAD_MODEL = "snakers4/silero-vad"
VAD_REPO_OR_DIR = "snakers4/silero-vad"

class AudioProcessor:
    def __init__(self, model_size="distil-whisper-large-v3", device="auto", compute_type="default"):
        self.device = "cuda" if torch.cuda.is_available() and device == "auto" else "cpu"
        # On Mac, MPS is available but faster-whisper (CTranslate2) might not fully support it natively out of the box without specific compilation, using CPU for VAD but auto for whisper
        
        # Load VAD
        try:
            self.vad_model, utils = torch.hub.load(repo_or_dir=VAD_REPO_OR_DIR,
                                                   model='silero_vad',
                                                   force_reload=False)
            self.vad_model.to(self.device)
            self.get_speech_timestamps = utils[0]
            self.vad_iterator = utils[3]
        except Exception as e:
            print(f"Error loading Silero VAD: {e}")
            self.vad_model = None

        # Load Faster-Whisper
        try:
            self.whisper_model = WhisperModel(model_size, device=self.device, compute_type=compute_type)
        except Exception as e:
            print(f"Error loading Faster-Whisper: {e}")
            self.whisper_model = None
            
        self.audio_buffer = np.array([], dtype=np.float32)
        self.sample_rate = 16000 # Standard for Whisper and Silero
        
    def process_audio_chunk(self, audio_chunk_bytes: bytes) -> str:
        """
        Takes raw PCM 16-bit 16kHz mono audio bytes, 
        checks for voice activity, and transcribes if voice is present.
        Returns the transcribed text or empty string.
        """
        if not self.whisper_model or not self.vad_model:
            return ""
            
        # Convert bytes to numpy array
        chunk = np.frombuffer(audio_chunk_bytes, dtype=np.int16).astype(np.float32) / 32768.0
        
        # Append to buffer
        self.audio_buffer = np.concatenate((self.audio_buffer, chunk))
        
        # We need at least some amount of audio to process (e.g. 1-2 seconds)
        if len(self.audio_buffer) < self.sample_rate * 2: # 2 seconds
            return ""
            
        # Check for voice activity
        audio_tensor = torch.from_numpy(self.audio_buffer).to(self.device)
        
        # Get speech timestamps
        speech_timestamps = self.get_speech_timestamps(audio_tensor, self.vad_model, sampling_rate=self.sample_rate)
        
        if not speech_timestamps:
            # No voice detected, clear buffer and return
            self.audio_buffer = np.array([], dtype=np.float32)
            return ""
            
        # Voice detected, let's transcribe
        # In a real streaming scenario, we'd wait for a silence pause to transcribe a full segment, 
        # but for this iteration, we transcribe what we have and clear.
        
        segments, info = self.whisper_model.transcribe(self.audio_buffer, beam_size=5, language="es")
        
        transcription = ""
        for segment in segments:
            transcription += segment.text + " "
            
        # Clear buffer after transcription (naive approach for MVP)
        self.audio_buffer = np.array([], dtype=np.float32)
        
        return transcription.strip()
