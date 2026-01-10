from deep_translator import GoogleTranslator
from langdetect import detect, DetectorFactory

DetectorFactory.seed = 0

class LanguageTools:
    def detect_language(self, text):
        try:
            return detect(text)
        except:
            return None

    def translate(self, text, src, dest):
        return GoogleTranslator(source=src, target=dest).translate(text)
