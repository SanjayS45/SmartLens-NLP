import serial
import time
import pyphen
from googletrans import Translator

class Translation:

    def translate_text(text, dest='en'):
        translator = Translator()
        translation = translator.translate(text, dest=dest)
        return translation.text

text = 'daijoubu'
translated_text = Translation.translate_text(text)
print(translated_text)


