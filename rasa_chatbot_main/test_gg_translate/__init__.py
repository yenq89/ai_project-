from googletrans import Translator

translator = Translator()
translated = translator.translate('Hello, world!', src='en', dest='vi')
print(translated.text)
