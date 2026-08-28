import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pywhispercpp.model import Model

MODEL_NAME = "large-v3-turbo-q5_0"
DEFAULT_WORKERS = 1
AUDIO_EXTS = ('.wav', '.m4a', '.mp3', '.webm')

def find_audio_files(path):
    return [os.path.join(path, f) for f in os.listdir(path) if f.lower().endswith(AUDIO_EXTS)]

def load_model():
    return Model(MODEL_NAME, print_realtime=False, print_progress=False)

def transcribe_file(model, file_path):
    segments = model.transcribe(file_path)
    text = "\n".join(segment.text.strip() for segment in segments)
    base = os.path.splitext(file_path)[0]
    out = f"{base}.txt"
    with open(out, 'w') as fp:
        fp.write(text)
    return file_path, out

def process_directory(path, model, max_workers):
    files = find_audio_files(path)
    if not files:
        print("no audio files found")
        return
    if max_workers == 1:
        for i, file in enumerate(files, 1):
            try:
                _, out = transcribe_file(model, file)
                print(f"[{i}/{len(files)}] {os.path.basename(file)} → {os.path.basename(out)}")
            except Exception as e:
                print(f"failed {os.path.basename(file)}: {e}")
    else:
        with ThreadPoolExecutor(max_workers=max_workers) as exe:
            futures = {exe.submit(transcribe_file, model, f): f for f in files}
            for i, fut in enumerate(as_completed(futures), 1):
                src = futures[fut]
                try:
                    _, out = fut.result()
                    print(f"[{i}/{len(futures)}] {os.path.basename(src)} → {os.path.basename(out)}")
                except Exception as e:
                    print(f"failed {os.path.basename(src)}: {e}")

def process_file(path, model):
    src, out = transcribe_file(model, path)
    print(f"{os.path.basename(src)} → {os.path.basename(out)}")

def main():
    path = input("Enter file or directory path: ").strip()
    if not os.path.exists(path):
        print(f"path not found: {path}")
        sys.exit(1)
    model = load_model()
    if os.path.isdir(path):
        process_directory(path, model, DEFAULT_WORKERS)
    else:
        process_file(path, model)

if __name__ == "__main__":
    main()
