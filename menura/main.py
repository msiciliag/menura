import flet as ft
from src.record import AudioRecorder
from src.transcript import AudioTranscriber

OUTPUT_PATH = "./media/output"
MODEL = "openai/whisper-large-v3"

def main(page: ft.Page):
    page.title = "Menura"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    recorder = AudioRecorder(OUTPUT_PATH)
    txt_transcript = ft.Text("", size=20)
    
    def start_recording(e):
        btn_start.disabled = True
        btn_stop.disabled = False
        recorder.start_recording()
        page.update()
    
    def stop_recording(e):
        btn_start.disabled = False
        btn_stop.disabled = True
        recorder.stop_recording()
        page.update()

    def transcribe_audio(e):
        btn_transcribe.disabled = True
        transcriber = AudioTranscriber(OUTPUT_PATH + ".wav", MODEL)
        transcript = transcriber.transcript()
        txt_transcript.value = transcript
        btn_transcribe.disabled = False
        page.update()

    btn_start = ft.ElevatedButton("Iniciar Grabación", on_click=start_recording)
    btn_stop = ft.ElevatedButton("Detener Grabación", on_click=stop_recording, disabled=True)
    btn_transcribe = ft.ElevatedButton("Transcribir", on_click=transcribe_audio)

    page.add(
        ft.Row(
            [btn_start, btn_stop, btn_transcribe],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        txt_transcript
    )

ft.app(target=main)