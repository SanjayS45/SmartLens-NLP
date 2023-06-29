
from google.cloud import speech_v1p1beta1 as speech
import os
import serial
import time

# defining serial object
port = 'COM4'
baud_rate = 9600
ser = serial.Serial(port, baud_rate, timeout=1)
time.sleep(2)

# google cloud key
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/vsid3/Downloads/speechtotext-390719-614f9b327af3.json"

import speech_recognition as sr
from nltk.tokenize import word_tokenize


# Initialize the recognizer
r = sr.Recognizer()
global token, tokens_before_end
token = 0
tokens_before_end = 'aaa'

# Define a function to recognize speech
def recognize_speech():
    with sr.Microphone() as source:
        print("Speak something...")
        audio = r.listen(source)

    try:
        # Use Google Speech Recognition to convert speech to text
        text = r.recognize_google(audio)
        #print("Recognized speech:", text)
        # Tokenize the recognized text using NLTK
        global tokens
        tokens = word_tokenize(text)
        print("Tokens:", tokens)
        
        # Keeps the serial open until the user wants to stop the conversation.
        while end_key_word != True:
            ser.write(text.encode())
            recognize_speech()
        ser.write(tokens_before_end.encode())
        '''
            for word in tokens:
            time.sleep(0.5)
            ser.write(word.encode() + " ".encode())
            time.sleep(0.6)
        '''
        ser.close()

    except sr.UnknownValueError:
        print("Speech recognition could not understand audio.")

def end_key_word():
    end = False
    tokens_before_end = ''
    for token in tokens:
        if token == 'end':
            return True
        else:
            tokens_before_end += token + ' '
    return end        
    
    
# Call the function to start speech recognition
recognize_speech()




