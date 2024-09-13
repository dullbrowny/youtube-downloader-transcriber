import whisper
import sys
import os

def transcribe_audio(file_path):
    # Load the base model (you can use "tiny", "base", "small", "medium", "large" as per your need)
    model = whisper.load_model("base")

    # Transcribe the audio file
    result = model.transcribe(file_path)

    # Extract the file name without the extension
    file_name = os.path.splitext(file_path)[0]

    # Write the transcription to a .notes file
    output_file = f"{file_name}.notes"
    with open(output_file, "w") as f:
        f.write(result["text"])

    print(f"Transcription saved to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python transcribe.py <path_to_audio_file>")
    else:
        audio_file = sys.argv[1]
        if os.path.exists(audio_file):
            transcribe_audio(audio_file)
        else:
            print(f"Error: File '{audio_file}' not found.")

