import os
import sys
import argparse
import whisper
from concurrent.futures import ThreadPoolExecutor, as_completed

def find_audio_files(path):
    exts = ('.wav', '.m4a', '.mp3', '.webm')
    return [os.path.join(path, f) for f in os.listdir(path) if f.lower().endswith(exts)]

def transcribe_file(model, file_path):
    result = model.transcribe(file_path)
    base = os.path.splitext(file_path)[0]
    out = f"{base}.txt"
    with open(out, 'w') as fp:
        fp.write(result['text'])
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

def load_model(size):
    try:
        return whisper.load_model(size)
    except ValueError:
        print(f"Could not load model '{size}', defaulting to large")
        return whisper.load_model("large")

def main():
    path = input("Enter file or directory path: ").strip()
    p = argparse.ArgumentParser()
    p.add_argument("--model", default="large", help="whisper model size")
    p.add_argument("--workers", type=int, default=1, help="max parallel tasks")
    args = p.parse_args()
    if not os.path.exists(path):
        print(f"path not found: {path}")
        sys.exit(1)
    model = load_model(args.model)
    if os.path.isdir(path):
        process_directory(path, model, args.workers)
    else:
        process_file(path, model)

if __name__ == "__main__":
    main()

