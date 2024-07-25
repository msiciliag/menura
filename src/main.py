import whisper

model = whisper.load_model("base")
result = model.transcribe("../media/audio.mp3")
print(result["text"])