'''

@author: Sanjay Sundaram
@date: 07/06/2023
@version: 1.0

MIT License

Copyright (c) 2023 Sanjay Sundaram

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

'''

from google.cloud import speech_v1p1beta1 as speech
import os
import serial
import time
import threading
import speech_recognition as sr
from nltk.tokenize import word_tokenize
from google.cloud import translate_v2 as translate
from langcodes import Language
from googletrans import Translator


# This provides a real-time speech-to-text transcription with a translation feature compatible with most languages.
class SpeechToText:
    global ser, lang, exit_flag, tokens_before_end, token, check_done, check_deactivated, ser_setup, activate_translation, lang, translate_client

    def __init__(self):
        pass
        
    # defining serial object
    def serial_setup():
        global ser, ser_setup
        port = 'COM4'
        baud_rate = 9600
        ser = serial.Serial(port, baud_rate, timeout=1)
        ser_setup = True
        time.sleep(1)
    
    # Global variable declarations
    exit_flag = True
    token = 0
    check_done = False
    check_deactivated = False
    ser_setup = False
    activate_translation = False
    #to_lang_key = 'en'
    from_language = "English"
    to_language = "English"
    # google cloud key
    #os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/vsid3/Downloads/speechtotext-390719-cc673dfdfa9a.json"
    #translate_client = translate.Client.from_service_account_json('C:/Users/vsid3/Downloads/speechtotext-390719-cc673dfdfa9a.json')

    #os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:\Users\vsid3\AppData\Roaming\gcloud\application_default_credentials.json"
    #translate_client = translate.Client.from_service_account_json('C:/Users/vsid3/AppData/Roaming/gcloud/application_default_credentials.json')
    translate_client = translate.Client.from_service_account_json('C:/Users/vsid3/Downloads/speechtotext-390719-adbb4781ca18.json')

    # Define a function to recognize speech
    def recognize_speech():
        global ser, text
        if ser_setup == False:
            SpeechToText.serial_setup()
        # Initialize the recognizer
        r = sr.Recognizer()
    
        # Capture audio input
        with sr.Microphone() as source:
            print("Speak something...")
            audio = r.listen(source)
        try:
            # Use Google Speech Recognition to convert speech to text
            text = r.recognize_google(audio)
            print("Recongized:", text)
            split_text = text.split()
            not_last_word = ' '.join(split_text[0:2])
            if not_last_word == "translate from":
                try:
                    my_sp.translation(split_text[-1], split_text[2])
                except Exception as e:
                    print("What would you like to translate it to?")
            elif activate_translation:
                my_sp.translation(to_language, from_language)
            
            # Tokenize the recognized text using NLTK
            global tokens
            tokens = word_tokenize(text)
            # Prints messages to the OLED until the user wants to stop the conversation.
            SpeechToText.start_key_word()
            if check_deactivated == False and check_done == True and SpeechToText.end_key_word() == False:
                print(tokens)
                ser.write(' '.join(tokens).encode())
            elif SpeechToText.end_key_word() == True:
                ser.write(tokens_before_end.encode())
                ser.write("\n\nVoice Recognition is shutting down...".encode())
        
        # If the audio isn't detected then the user is notified
        except sr.UnknownValueError:
            print("Speech recognition could not understand audio.")

    # Defines the deactivation key word
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

    # Defines the activation key word
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
    
    def translation(self, to_lang, from_lang):
        global text, translate_client, activate_translation, to_language, from_language
        
        translator = Translator()
        to_language = to_lang
        from_language = from_lang
        to_lang_key = str(Language.find(to_language))
        from_lang_key = str(Language.find(from_language))
        translation = translator.translate(text, dest=to_lang_key, src=from_lang_key)
        activate_translation = True
        text = translation.text
        print(f'{to_language}: {text}')
        '''
        to_language = to_lang
        from_language = from_lang
        to_lang_key = str(Language.find(to_language))
        from_lang_key = str(Language.find(from_language))
        #text = json.dumps(translate_client.translate(values=text, to_language=lang))
        text = translate_client.translate(values=text, target_language=to_lang_key, source_language=from_lang_key)['translatedText']
        activate_translation = True
        print(text)'''
        
# Listens for activity on the main thread and continues asking for audio input.
def listener_thread_function():
   while exit_flag == True:
        SpeechToText.recognize_speech()
my_sp = SpeechToText()       
listener_thread = threading.Thread(target=listener_thread_function)
listener_thread.start()
listener_thread.join(timeout=1000)
print(f"THE THREAD IS ALIVE: {listener_thread.is_alive()}")


# IMPORTANT INFORMATION !!!
# Error: Translation only happening one way: English --> foreign language, NOT VICE VERSA
# Failed attempt(s): defined source language parameter on line 153 (no error message was returned when code was executed, just not functioning as intended).
#                    created a seperate translator, it is now able to romanize for most non-latin languages, but limited to basic phrases. 
