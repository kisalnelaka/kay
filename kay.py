import os
import shutil
from pathlib import Path
import re
import speech_recognition as sr
import pyttsx3

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Configure voice settings
voices = engine.getProperty('voices')
# Set male voice (usually index 0 is male)
engine.setProperty('voice', voices[0].id)
# Set speaking rate (default is 200)
engine.setProperty('rate', 175)

def speak(text):
    """Speak the provided text aloud."""
    print("Kay:", text)
    engine.say(text)
    engine.runAndWait()

def listen():
    """Listen to a voice command and return it as a lower-case string."""
    r = sr.Recognizer()
    try:
        # List available microphones
        print("Available microphones:", sr.Microphone.list_microphone_names())
        
        # Find the JBL Tune 720BT microphone
        mic_index = None
        for index, name in enumerate(sr.Microphone.list_microphone_names()):
            if "JBL Tune 720BT" in name and "Hands-Free" in name:
                mic_index = index
                break
        
        if mic_index is None:
            speak("Could not find JBL headset microphone. Using default microphone.")
            mic_index = 0
        
        print(f"Using microphone: {sr.Microphone.list_microphone_names()[mic_index]}")
        
        with sr.Microphone(device_index=mic_index) as source:
            print("Adjusting for ambient noise...")
            r.adjust_for_ambient_noise(source, duration=2)
            r.energy_threshold = 1000  # Lower threshold for better sensitivity
            r.dynamic_energy_threshold = True
            r.pause_threshold = 0.8  # Shorter pause threshold
            speak("Listening...")
            try:
                audio = r.listen(source, timeout=5, phrase_time_limit=10)
                print("Audio captured, processing...")
            except sr.WaitTimeoutError:
                speak("No speech detected. Please try again.")
                return ""
    except Exception as e:
        speak(f"Error accessing microphone: {str(e)}")
        print("Microphone Error Details:", str(e))
        return ""

    try:
        command = r.recognize_google(audio)
        print("You said:", command)
        return command.lower()
    except sr.UnknownValueError:
        speak("I didn't catch that. Please try again.")
        return ""
    except sr.RequestError as e:
        speak("There was an issue with the speech service.")
        print("Speech Service Error Details:", str(e))
        return ""

def list_files(directory):
    """List all files in the given directory."""
    try:
        p = Path(directory)
        if not p.exists():
            speak(f"The directory {directory} does not exist.")
            return
        files = [f.name for f in p.iterdir() if f.is_file()]
        if files:
            speak("Files in " + directory + " are: " + ", ".join(files))
        else:
            speak("No files found in " + directory)
    except Exception as e:
        speak("Error listing files: " + str(e))

def list_dirs(directory):
    """List all subdirectories in the given directory."""
    try:
        p = Path(directory)
        if not p.exists():
            speak(f"The directory {directory} does not exist.")
            return
        dirs = [d.name for d in p.iterdir() if d.is_dir()]
        if dirs:
            speak("Directories in " + directory + " are: " + ", ".join(dirs))
        else:
            speak("No directories found in " + directory)
    except Exception as e:
        speak("Error listing directories: " + str(e))

def rename_item(old_name, new_name):
    """Rename a file or directory from old_name to new_name."""
    try:
        os.rename(old_name, new_name)
        speak(f"Renamed {old_name} to {new_name}.")
    except Exception as e:
        speak("Error renaming: " + str(e))

def delete_file(filename):
    """Delete a file."""
    try:
        if os.path.isfile(filename):
            os.remove(filename)
            speak(f"Deleted file {filename}.")
        else:
            speak(f"File {filename} does not exist.")
    except Exception as e:
        speak("Error deleting file: " + str(e))

def delete_folder(foldername):
    """Delete a folder and all its contents."""
    try:
        if os.path.isdir(foldername):
            shutil.rmtree(foldername)
            speak(f"Deleted folder {foldername}.")
        else:
            speak(f"Folder {foldername} does not exist.")
    except Exception as e:
        speak("Error deleting folder: " + str(e))

def move_item(source, destination):
    """Move a file or directory to a new location."""
    try:
        shutil.move(source, destination)
        speak(f"Moved {source} to {destination}.")
    except Exception as e:
        speak("Error moving item: " + str(e))

def copy_item(source, destination):
    """Copy a file or directory to a new location."""
    try:
        if os.path.isfile(source):
            shutil.copy2(source, destination)
            speak(f"Copied file {source} to {destination}.")
        elif os.path.isdir(source):
            shutil.copytree(source, destination)
            speak(f"Copied folder {source} to {destination}.")
        else:
            speak("Source does not exist.")
    except Exception as e:
        speak("Error copying item: " + str(e))

def open_file(filename):
    """Open a file using the default application (Windows only)."""
    try:
        if os.name == 'nt':
            os.startfile(filename)
            speak(f"Opening {filename}.")
        else:
            speak("Open file command is currently only supported on Windows.")
    except Exception as e:
        speak("Error opening file: " + str(e))

def show_help():
    """Display all available commands and their usage."""
    help_text = """
Available commands:
- list : List all files in the current directory
- list files in [directory] : List all files in the specified directory
- list folders in [directory] : List all folders in the specified directory
- rename [old_name] to [new_name] : Rename a file or folder
- delete file [filename] : Delete a specific file
- delete folder [foldername] : Delete a folder and its contents
- move [source] to [destination] : Move a file or folder to a new location
- copy [source] to [destination] : Copy a file or folder to a new location
- open file [filename] : Open a file with its default application
- help : Show this help message
- exit or quit : Exit the program
    """
    speak(help_text)

def process_command(command):
    """Parse and execute a command based on keywords."""
    if command == "help":
        show_help()
    elif command == "list":
        # Simple command to list files in current directory
        list_files(".")
    elif "list files" in command:
        # Expected: "list files in [directory]" (default to current directory)
        m = re.search(r"list files in (.+)", command)
        directory = m.group(1).strip() if m else "."
        list_files(directory)
    elif "list folders" in command or "list directories" in command:
        m = re.search(r"list (folders|directories) in (.+)", command)
        directory = m.group(2).strip() if m else "."
        list_dirs(directory)
    elif "rename" in command:
        # Expected: "rename old_name to new_name"
        m = re.search(r"rename (.+?) to (.+)", command)
        if m:
            old_name = m.group(1).strip()
            new_name = m.group(2).strip()
            rename_item(old_name, new_name)
        else:
            speak("Sorry, I couldn't understand the rename command.")
    elif "delete file" in command:
        m = re.search(r"delete file (.+)", command)
        if m:
            filename = m.group(1).strip()
            delete_file(filename)
        else:
            speak("Sorry, I couldn't understand which file to delete.")
    elif "delete folder" in command or "delete directory" in command:
        m = re.search(r"delete (folder|directory) (.+)", command)
        if m:
            foldername = m.group(2).strip()
            delete_folder(foldername)
        else:
            speak("Sorry, I couldn't understand which folder to delete.")
    elif "move" in command:
        # Expected: "move source to destination"
        m = re.search(r"move (.+?) to (.+)", command)
        if m:
            source = m.group(1).strip()
            destination = m.group(2).strip()
            move_item(source, destination)
        else:
            speak("Sorry, I couldn't parse the move command.")
    elif "copy" in command:
        # Expected: "copy source to destination"
        m = re.search(r"copy (.+?) to (.+)", command)
        if m:
            source = m.group(1).strip()
            destination = m.group(2).strip()
            copy_item(source, destination)
        else:
            speak("Sorry, I couldn't parse the copy command.")
    elif "open file" in command:
        m = re.search(r"open file (.+)", command)
        if m:
            filename = m.group(1).strip()
            open_file(filename)
        else:
            speak("Sorry, I couldn't understand which file to open.")
    elif "exit" in command or "quit" in command:
        speak("Goodbye!")
        exit(0)
    else:
        speak("Sorry, I did not recognize that command.")

def main():
    speak("Hello Kisal, I am Kay, your personal file management assistant. I'm here to help you organize and manage your files. Just say 'help' if you need to know what I can do.")
    while True:
        command = listen()
        if command:
            process_command(command)

if __name__ == "__main__":
    main()
