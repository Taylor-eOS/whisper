To run this code on a computer, you need to set up a Python environment and install the necessary dependencies (like OpenAI's Whisper model). Here’s a step-by-step guide for both Linux and Windows users who are unfamiliar with Python.

### Installing Python

1. **Linux:** Python is often pre-installed. Check if it’s installed by opening a terminal and typing `python3 --version`. If you see a version number, Python is installed. If not, install Python by running `sudo apt update` followed by `sudo apt install python3 python3-pip`.
   
2. **Windows:** Go to the official Python website (https://python.org), download the installer, run it, and make sure to select the option to "Add Python to PATH" during installation. Verify by opening Command Prompt and typing `python --version`.

### Setting Up the Code

For setting up the environment to run the script with Whisper, follow these steps:

1. **Install `pip`**:
   - **Linux**: Open a terminal and type:
     ```
     sudo apt update
     sudo apt install python3-pip
     ```
   - **Windows**: Python's installer typically includes `pip`. Verify it’s installed by typing `pip --version` in Command Prompt. If it's not installed, re-run the Python installer and ensure "Install pip" is selected.

2. **Create a Virtual Environment**:
   - Virtual environments allow you to install packages in an isolated space specific to this project.
   - **Linux**: In the terminal, navigate to the directory where you want to create the environment (where the `whis.py` script is). Then run:
     ```
     python3 -m venv whisper
     ```
   - **Windows**: Open Command Prompt, navigate to the desired directory, and type:
     ```
     python -m venv whisper
     ```
   - This creates a virtual environment called `whisper` in the current directory.

3. **Activate the Virtual Environment**:
   - **Linux**: Run
     ```
     source whisper/bin/activate
     ```
   - **Windows**: Run
     ```
     whisper\Scripts\activate
     ```
   - Once activated, the terminal prompt should change, indicating you’re now working within the virtual environment.

4. **Install Required Packages**:
   - With the virtual environment activated, install Whisper along with all necessary dependencies by running:
     ```
     pip install openai-whisper
     ```
   - This command installs Whisper and any other packages it needs.

### Running the Code

1. **Save the Script**: Clone the repository, download the file, or copy the code into a file called `whis.py`.

2. **Organize Your Audio Files**: Place the audio file(s) you want to transcribe into a single directory. Whisper supports `.wav`, `.m4a`, `.mp3`, and `.webm` formats.

3. **Running the Script**:
   - **Linux**: In the terminal, navigate to the folder where you saved `whis.py` using `cd /path/to/folder`.
   - **Windows**: Open Command Prompt, navigate to the folder with `whis.py` using `cd \path\to\folder`.

4. **Execute the Script**: Run the script by typing:
   ```
   python whis.py <directory_path> [model_size]
   ```
   - Replace `<directory_path>` with the path to the directory containing your audio files or the filename of the file you want to transcribe.
   - `[model_size]` is optional and defines the size of the Whisper model to use. Options include `tiny`, `base`, `small`, `medium`, `large`, or `large-v2`. The default is `medium` if no size is specified, which is a good compromize between how long it will take and accuracy.

### How the Script Works

The script is designed to take a single file or a directory path containing audio files and transcribe each file. Here's a breakdown of the process:

- **Loading the Model**: The script first tries to load the Whisper model specified by the user. If there’s an issue with the model size input, it defaults to `medium`.
  
- **File Processing**: It lists all audio files in the specified directory and checks if the directory contains valid files. For each audio file, it uses the Whisper model to generate a transcription.

- **Saving the Transcription**: For each audio file, it saves the transcription to a text file with the same name as the audio file but with "_transcript.txt" appended.

- **Single File Option**: If the specified path points to a single audio file instead of a directory, the script transcribes that one file.

### Troubleshooting Common Issues

- **Missing Dependencies**: Ensure Whisper and other dependencies are installed (`pip install whisper`).
- **File Paths**: If you encounter errors related to paths, ensure your path is formatted correctly and that the files exist.
- **Python Version**: Whisper requires Python 3.7 or later, so ensure you’re not using an older version.

After the script runs, the transcriptions for each file will be saved in the same location as the audio files, with each transcription in a separate text file named accordingly.
