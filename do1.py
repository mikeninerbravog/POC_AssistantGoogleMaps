"""
Bootcamp: BairesDev - Machine Learning Practitioner - February 2025
Proof of Concept - "Virtual Assistant Creation"
"""

# Import the necessary libraries
import speech_recognition as sr # For speech recognition (Speech-to-Text)
from gtts import gTTS           # For text-to-speech conversion (Text-to-Speech)
import playsound                # To play generated audio
import webbrowser               # To open URLs in the browser
import os                       # For file manipulation (removing old audio)

# Function 1: Convert text to speech (Text-to-Speech - TTS)
def text_to_speech(text):
    """
    Converts text to audio and plays the message.
    
    Parameters:
    text (str): The text to be converted to speech.
    
    Return:
    None. It just plays the audio.
    """
    tts = gTTS(text=text, lang='pt')  # Convert text to audio in Portuguese
    filename = "voice.mp3"  # Output file name

    # Remove the previous file to avoid conflict
    try:
        os.remove(filename)
    except OSError:
        pass

    # Saves and plays audio
    tts.save(filename)
    playsound.playsound(filename)

# Function 2: Capture speech and convert to text (Speech-to-Text - STT)
def speech_to_text():
    """
    Captures the user's speech through the microphone and converts it to text.
    
    Return:
    str: The text recognized by the AI.
    None: If speech could not be recognized.
    """
    recognizer = sr.Recognizer()  # Initialize the audio recognizer

    with sr.Microphone() as source:                              # Access the system microphone
        recognizer.pause_threshold = 1                           # Wait up to 1 second of silence before processing speech
        recognizer.adjust_for_ambient_noise(source, duration=1)  # Adjusts for ambient noise

        print("Ouvindo...")  # Indicates that it is capturing audio

        try:
            audio = recognizer.listen(source)  # Captures the user's audio
            text = recognizer.recognize_google(audio, language="pt-BR").lower()  # Converts speech to text

            print(f"You said: {text}")  # Displays the output in the terminal
            return text  # Returns the recognized text

        except sr.UnknownValueError:  # If you don't understand speech
            text_to_speech("Sorry, I don't understand. Please try again.")
            return None
        except sr.RequestError:  # If there is an error in the recognition API
            text_to_speech("Error in the speech recognition service.")
            return None

# Function 3: Generate search on Google Maps
def search_on_google_maps(query):
    """
    Generates a Google Maps search from the captured text.
    
    Parameters:
    query(str): The search term to search for on Google Maps.
    
    Return:
    None. Just open the browser with the search.
    """
    if query:
        text_to_speech(f"OK, looking for {query}")           # Confirm the search before opening
        url = f"https://www.google.com/maps/search/{query}/"    # Generates the survey URL
        webbrowser.open(url)                                    # Open the browser with the search

# Main Function: Loop to capture and process commands continuously
def main():
    """
    Main function that keeps the virtual assistant in a continuous loop,
    listening and responding to the user until it is prompted to terminate.
    """
    text_to_speech("Hello! What do you want to search for on Google Maps?")  # Initial message

    while True:
        user_input = speech_to_text()  # Captures what the user has said

        if user_input:                                      # If you captured any lines
            if user_input in ["fim", "encerrar", "sair"]:   # If the user asks to leave
                text_to_speech("Encerrando. Até logo!")     # Farewell message
                break                                       # Exit the loop and end the program
            
            search_on_google_maps(user_input)               # Runs the search on Google Maps

# Runs the script only if it is run directly (and not imported as a module)
if __name__ == "__main__":
    main()
