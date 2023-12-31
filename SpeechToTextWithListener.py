from google.cloud import speech_v1p1beta1 as speech
import os
import serial
import time
import threading


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
global token
exit_flag = True
token = 0
global check_done, check_deactivated
check_done = False
check_deactivated = False
# Define a function to recognize speech
def recognize_speech():
    global exit_flag, tokens_before_end
    with sr.Microphone() as source:
        print("Speak something...")
        audio = r.listen(source)
    try:
        # Use Google Speech Recognition to convert speech to text
        text = r.recognize_google(audio)
        print("Recongized:", text)
        #ser.write(text.encode())
        # Tokenize the recognized text using NLTK
        global tokens
        tokens = word_tokenize(text)
        
        # Prints messages to the OLED until the user wants to stop the conversation.
        start_key_word()
        end_key_word()
        if check_deactivated == False and check_done == True and end_key_word() == False:
            ser.write(' '.join(tokens).encode())
        elif end_key_word() == True:
            ser.write(tokens_before_end.encode())
            ser.write("\n\nVoice Recognition is shutting down...".encode())
        
            
    except sr.UnknownValueError:
        print("Speech recognition could not understand audio.")

def end_key_word():
    global tokens_before_end, check_deactivated, check_done
    end = False
    tokens_before_end = ''
    for token in tokens:
        if token == 'deactivate':
            check_deactivated = True
            check_done = False
            return True
        else:
            tokens_before_end += token + ' '
            continue
    return end      

def start_key_word():
    global check_done, check_deactivated, tokens
    end_start = False
    index = 0
    for token in tokens:
        if token == 'activate':
            index = tokens.index(token)
            check_deactivated = False
            if check_done == False:
                tokens = tokens[index+1:]
                check_done = True
            return True
        else:
            continue
    return end_start   

def listener_thread_function():
   while exit_flag == True:
        recognize_speech()
        
listener_thread = threading.Thread(target=listener_thread_function)
listener_thread.start()