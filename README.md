# Kay - Voice-Controlled File Management Assistant

Kay is a Python-based voice assistant that helps you manage files and folders using voice commands. It uses speech recognition to understand your commands and text-to-speech to provide feedback.

## Features

- Voice command recognition
- File and folder management
- Natural language processing
- Text-to-speech feedback
- Cross-platform support (with some Windows-specific features)

## Requirements

- Python 3.6 or higher
- SpeechRecognition
- pyttsx3
- PyAudio (for microphone input)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/kay.git
cd kay
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

Run the program:
```bash
python kay.py
```

Kay will greet you and start listening for commands. Here are the available commands:

### File and Folder Listing
- `list` - List all files in the current directory
- `list files in [directory]` - List all files in the specified directory
- `list folders in [directory]` - List all folders in the specified directory

### File Operations
- `rename [old_name] to [new_name]` - Rename a file or folder
- `delete file [filename]` - Delete a specific file
- `delete folder [foldername]` - Delete a folder and its contents
- `move [source] to [destination]` - Move a file or folder to a new location
- `copy [source] to [destination]` - Copy a file or folder to a new location
- `open file [filename]` - Open a file with its default application (Windows only)

### System Commands
- `help` - Show the list of available commands
- `exit` or `quit` - Exit the program

## Examples

- "list files in Documents"
- "rename old_file.txt to new_file.txt"
- "delete file test.txt"
- "move file.txt to Documents"
- "copy folder1 to backup"
- "open file report.pdf"

## Notes

- The program requires an active internet connection for speech recognition
- Some commands (like `open file`) are currently only supported on Windows
- Make sure your microphone is properly configured before using voice commands

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is licensed under the MIT License - see the LICENSE file for details.
