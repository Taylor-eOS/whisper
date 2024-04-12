import whisper
import sys
import os

def transcribe_audio(input_audio_path: str):
    # Load the model
    model = whisper.load_model("base")  # Options: "tiny", "small", "base", "medium", "large"

    # Process the audio file
    result = model.transcribe(input_audio_path)

    # Extract the transcription text
    transcription = result["text"]

    # Generate output text file path
    base_name = os.path.splitext(input_audio_path)[0]
    output_text_path = f"{base_name}_transcript.txt"

    # Save the transcription to a file
    with open(output_text_path, "w") as text_file:
        text_file.write(transcription)

    print(f"Done! Transcription saved to {output_text_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script_name.py <audio_file_path>")
    else:
        input_audio_path = sys.argv[1]
        transcribe_audio(input_audio_path)

