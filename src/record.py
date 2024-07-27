import pyaudio
import wave
from pynput import keyboard

from pydub import AudioSegment
from pydub.silence import detect_nonsilent



class AudioRecorder:
    def __init__(self, output_path, format=pyaudio.paInt16, channels=1, rate=16000, frames_per_buffer=1024):
        self.output_path = output_path
        self.format = format
        self.channels = channels
        self.rate = rate
        self.frames_per_buffer = frames_per_buffer
        self.frames = []
        self.audio = pyaudio.PyAudio()
        self.stream = None

    def start_recording(self):
        self.stream = self.audio.open(format=self.format, channels=self.channels, rate=self.rate, input=True, frames_per_buffer=self.frames_per_buffer, stream_callback=self.callback)
        self.stream.start_stream()
        print("Recording... Press 's' to stop.")

    def callback(self, in_data, frame_count, time_info, status):
        self.frames.append(in_data)
        return (in_data, pyaudio.paContinue)

    def stop_recording(self):
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()

        sound_file = wave.open(self.output_path, "wb")
        sound_file.setnchannels(self.channels)
        sound_file.setsampwidth(self.audio.get_sample_size(self.format))
        sound_file.setframerate(self.rate)
        sound_file.writeframes(b''.join(self.frames))
        sound_file.close()

        audio = AudioSegment.from_file(self.output_path)
        nonsilent_ranges = detect_nonsilent(audio, min_silence_len=1000, silence_thresh=-40)
        
        # Concatenate nonsilent segments
        nonsilent_audio = AudioSegment.empty()
        for start, end in nonsilent_ranges:
            nonsilent_audio += audio[start:end]
        
        nonsilent_audio.export(self.output_path + "-processed", format="wav")

        print(f"Audio recorded and saved to {self.output_path}")

    def end_recording(self, key):
        try:
            if key.char == 's':
                print("Stopping recording.")
                return False
        except AttributeError:
            pass
    
    
