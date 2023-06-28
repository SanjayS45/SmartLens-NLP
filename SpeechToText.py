
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
'''
# Converts speech in audio file to text
def transcribe_speech(audio):
    client = speech.SpeechClient()
    with open(audio, 'rb') as aud:
        cont = aud.read()
        
    recognizer = speech.RecognitionAudio(content=cont)
    configure = speech.RecognitionConfig(encoding = speech.RecognitionConfig.AudioEncoding.LINEAR16, language_code = 'en-US')
    response = client.recognize(config=configure, audio=recognizer)
    command = ""
   
   # Gathering results, printing transcript to terminal, and sending transcript to serial port to display on OLED.
    for result in response.results:
        transcription = result.alternatives[0].transcript
        words = transcription.split()
        print(words)
        for word in words:
            time.sleep(0.6)
            word += ' '
            ser.write(word.encode())
            time.sleep(0.5)
        ser.close()

# Locating the audio file  
path = "C:/Users/vsid3/Downloads/"    
raw_audio_file = path + "Trailer.wav"
transcribe_speech(raw_audio_file)
'''

import speech_recognition as sr
from nltk.tokenize import word_tokenize


# Initialize the recognizer
r = sr.Recognizer()

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
        tokens = word_tokenize(text)
        print("Tokens:", tokens)
        
        ser.write(text.encode())
        '''
        for word in tokens:
            time.sleep(0.5)
            ser.write(word.encode() + " ".encode())
            time.sleep(0.6)
        '''
        ser.close()

    except sr.UnknownValueError:
        print("Speech recognition could not understand audio.")
        
# Call the function to start speech recognition
recognize_speech()
print('yo')




