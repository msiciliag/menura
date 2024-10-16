import os
import pyaudio
import wave
from pynput import keyboard


class AudioRecorder:
    def __init__(self, output_path, format=pyaudio.paInt16, channels=1, rate=44100, frames_per_buffer=1024):
        
        dir_path = os.path.dirname(output_path)
        if dir_path and not os.path.exists(dir_path):
            os.makedirs(dir_path)


        self.output_path = output_path + ".wav"
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
        print("Recording... Press 'enter' to stop.")

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
        
        print(f"Audio recorded and saved to {self.output_path}")

    def end_recording(self, key):
        try:
            if key == keyboard.Key.enter:
                print("Stopping recording.")
                return False
        except AttributeError:
            pass
    