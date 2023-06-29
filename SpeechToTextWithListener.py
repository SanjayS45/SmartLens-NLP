from google.cloud import speech_v1p1beta1 as speech
import os
import serial
import time
import threading

git
# defining serial object
port = 'COM4'
baud_rate = 9600
ser = serial.Serial(port, baud_rate, timeout=1)
time.sleep(2)
exit_flag = True

# google cloud key
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/vsid3/Downloads/speechtotext-390719-614f9b327af3.json"

import speech_recognition as sr
from nltk.tokenize import word_tokenize


# Initialize the recognizer
r = sr.Recognizer()
global token, tokens_before_end, end_start
#end_start = False
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
        print(text)
        #print("Recognized speech:", text)
        # Tokenize the recognized text using NLTK
        global tokens
        tokens = word_tokenize(text)
        end_start = False
        
        while start_key_word() == True and end_start == False:
            print("Tokens:", tokens)
            # Keeps the serial open until the user wants to stop the conversation.
            while end_key_word() != True:
                
                ser.write(text.encode())
                with sr.Microphone() as source:
                    print("Speak something...")
                    audio = r.listen(source)
                    text = r.recognize_google(audio)
                    tokens = word_tokenize(text)
            end_start = True
            #ser.write(tokens_before_end.encode())
            
            ser.close()
            exit_flag = False
        

    except sr.UnknownValueError:
        print("Speech recognition could not understand audio.")

def end_key_word():
    end = False
    tokens_before_end = ''
    for token in tokens:
        if token == 'Stop':
            return True
        else:
            tokens_before_end += token + ' '
    return end      

def start_key_word():
    end_start = False
    for token in tokens:
        print(token)
        if token == 'Alexa':
            return True
        else:
            continue
    return end_start   
    
    
# Call the function to start speech recognition
#recognize_speech()


# Define a function that will run in the listener thread
def listener_thread_function():
    # Add your code here to listen for incoming data or perform other tasks

   while exit_flag == True:
        recognize_speech()

# Create a Thread object with the target set to your listener_thread_function
listener_thread = threading.Thread(target=listener_thread_function)

# Start the listener thread
listener_thread.start()
