import subprocess
import sys
import os
import time

def transcript(wav_file_path, model_name):
    start_time = time.time()
    model = f"modules/whisper.cpp/models/ggml-{model_name}.bin"
    if not os.path.exists(model):
        print(f"Model {model_name} not found.")
        sys.exit(1)
   
    if not os.path.exists(wav_file_path):
        print(f"File {wav_file_path} not found.")
        sys.exit(1)

    process_command = f"modules/whisper.cpp/main --model {model} --file {wav_file_path} --output-txt --print-colors --language es"
    try:
        process = subprocess.run(process_command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(process.stdout.decode())
        
    except subprocess.CalledProcessError as e:
        print(e.stderr.decode())
    end_time = time.time()

    print(f"Transcripted in {end_time - start_time} seconds.")    


if __name__ == "__main__":
    transcript(sys.argv[1], sys.argv[2])
    sys.exit(1)