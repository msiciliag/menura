import subprocess
import sys
import os
import time

class AudioTranscriber:

    def __init__(self, wav_file_path, model_name):
        self.wav_file_path = wav_file_path
        self.model_name = model_name


    def transcript(self):
        start_time = time.time()
        model = f"modules/whisper.cpp/models/ggml-{self.model_name}.bin"
        if not os.path.exists(model):
            print(f"Model {self.model_name} not found.")
            sys.exit(1)
    
        if not os.path.exists(self.wav_file_path):
            print(f"File {self.wav_file_path} not found.")
            sys.exit(1)

        process_command = f"modules/whisper.cpp/main --model {model} --file {self.wav_file_path} --output-txt --print-colors --language es"
        try:
            process = subprocess.run(process_command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(process.stdout.decode())
            
        except subprocess.CalledProcessError as e:
            print(e.stderr.decode())
        end_time = time.time()

        print(f"Transcripted in {end_time - start_time} seconds.")    
    
