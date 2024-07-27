from record import AudioRecorder
from transcript import AudioTranscriber

from pynput import keyboard

OUTPUT_PATH = "./media/output.wav"
MODEL = "medium"


def handle_recording() -> None:
    recorder = AudioRecorder(OUTPUT_PATH)
    recorder.start_recording()

    with keyboard.Listener(on_press=lambda key: recorder.end_recording(key)) as listener:
        listener.join()

    recorder.stop_recording()
    

def handle_transcription() -> None:
    transcriber = AudioTranscriber(OUTPUT_PATH, MODEL)
    transcriber.transcript()
    


if __name__ == "__main__":
    handle_recording()
    handle_transcription()
