from googletrans import Translator

translator = Translator()


def translate_to_english(text):
    try:
        return translator.translate(text, dest="en").text
    except:
        return text


def translate_text(text, target="en"):
    try:
        return translator.translate(text, dest=target).text
    except:
        return text
