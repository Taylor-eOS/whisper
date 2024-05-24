import whisper
import sys
import os

def transcribe_audio(input_path: str, model_size: str):
    # Load the specified Whisper model or default to "small"
    try:
        model = whisper.load_model(model_size)
    except ValueError:
        print(f"Defaulting to 'small' model.")
        model = whisper.load_model("small") #tiny,base,small,medium,large,large-v2
    
    files_processed = 0
    # Filter for audio files only
    audio_files = [f for f in os.listdir(input_path) if f.endswith(('.wav', '.m4a', '.mp3', '.webm'))]
    total_files = len(audio_files)

    if total_files == 0:
        print("No audio files found in the specified directory.")
        return

    # Process each file in the directory
    for filename in audio_files:
        file_path = os.path.join(input_path, filename)
        print(f"Processing {filename}... ({files_processed + 1}/{total_files})")
        
        # Transcribe the audio file
        result = model.transcribe(file_path)
        transcription = result['text']

        # Generate output text file path
        base_name = os.path.splitext(file_path)[0]
        output_text_path = f"{base_name}_transcript.txt"

        # Save the transcription to a file
        try:
            with open(output_text_path, 'w') as text_file:
                text_file.write(transcription)
            print(f"Done! Transcription saved to {output_text_path}")
        except IOError as e:
            print(f"Failed to write transcription: {e}")
    
        files_processed += 1

if __name__ == "__main__":
    if len(sys.argv) == 2:
        input_path = sys.argv[1]
        model_size = "small"
    elif len(sys.argv) == 3:
        input_path = sys.argv[1]
        model_size = sys.argv[2]
    else:
        print("Usage: python whis.py <directory_path> [model_size]")
        sys.exit(1)

    # Check if the input path is a directory
    if os.path.isdir(input_path):
        transcribe_audio(input_path, model_size)
    elif os.path.isfile(input_path):
        # Process single file
        model = whisper.load_model(model_size)
        result = model.transcribe(input_path)
        transcription = result['text']
        output_text_path = f"{os.path.splitext(input_path)[0]}_transcript.txt"
        with open(output_text_path, 'w') as text_file:
            text_file.write(transcription)
        print(f"Done! Transcription saved to {output_text_path}")
    else:
        print(f"The provided path '{input_path}' is neither a file nor a directory.")
