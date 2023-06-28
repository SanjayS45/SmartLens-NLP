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

# Converts speech in audio file to text
def transcribe_speech(audio):
    client = speech.SpeechClient()
    with open(audio, 'rb') as aud:
        cont = aud.read()
        
    recognizer = speech.RecognitionAudio(content=cont)
    configure = speech.RecognitionConfig(encoding = speech.RecognitionConfig.AudioEncoding.LINEAR16, language_code = 'en-US')
    response = client.recognize(config=configure, audio=recognizer)
    command = ""
    
    # Testing voice recognition
    '''
    data = ser.readline().decode('utf-8').rstrip()  # Read a line of data from the serial port
    print(data)
    while data != "o":
        data += ser.readline().decode('utf-8').rstrip()
        print(data)
        command += data 
    '''
   
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



