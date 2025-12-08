from langdetect import detect, DetectorFactory

DetectorFactory.seed = 0


def detect_language(text):
    try:
        return detect(text)
    except:
        return "unknown"
