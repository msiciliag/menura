import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline


class AudioTranscriber:

    def __init__(self, wav_file_path, model_id):
        self.wav_file_path = wav_file_path
        self.model_id = model_id


    def transcript(self):
        device = "cuda:0" if torch.cuda.is_available() else "cpu"
        torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

        model = AutoModelForSpeechSeq2Seq.from_pretrained(
            self.model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
        )
        model.to(device)

        processor = AutoProcessor.from_pretrained(self.model_id)

        pipe = pipeline(
            "automatic-speech-recognition",
            model=model,
            tokenizer=processor.tokenizer,
            feature_extractor=processor.feature_extractor,
            torch_dtype=torch_dtype,
            device=device,
            
        )

        
        result = pipe(self.wav_file_path, return_timestamps=True, generate_kwargs={"language": "spanish"})
        print(result["text"])
    


