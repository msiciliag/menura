import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
import os

OUTPUT_PATH = "./transciptions/output.txt"
CACHE_MODEL = "./cache_models"

class AudioTranscriber:
    def __init__(self, wav_file_path, model_id):
        self.wav_file_path = wav_file_path
        self.model_id = model_id

    def save_transcript(self, transctiption_output):
        if os.path.exists(OUTPUT_PATH):
            os.remove(OUTPUT_PATH)

        with open(OUTPUT_PATH, "w") as f:
            f.write(transctiption_output)

        print("Transcript saved successfully.")

    def transcript(self):
        os.makedirs(CACHE_MODEL, exist_ok=True)  # Crea la carpeta si no existe

        device = "cuda:0" if torch.cuda.is_available() else "cpu"
        torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

        # Carga el modelo desde la carpeta CACHE_MODEL
        model = AutoModelForSpeechSeq2Seq.from_pretrained(
            self.model_id, 
            torch_dtype=torch_dtype, 
            low_cpu_mem_usage=True, 
            use_safetensors=True, 
            cache_dir=CACHE_MODEL
        )
        model.to(device)

        processor = AutoProcessor.from_pretrained(self.model_id, cache_dir=CACHE_MODEL)

        pipe = pipeline(
            "automatic-speech-recognition",
            model=model,
            tokenizer=processor.tokenizer,
            feature_extractor=processor.feature_extractor,
            torch_dtype=torch_dtype,
            device=device,
        )
        try:
            result = pipe(self.wav_file_path, return_timestamps=True, generate_kwargs={"language": "spanish"})
            self.save_transcript(result["text"])
        except Exception as e:
            print("An error occurred while transcribing the audio.\n" + str(e))