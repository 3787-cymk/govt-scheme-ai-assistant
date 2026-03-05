import google.generativeai as genai
from google.cloud import texttospeech


def tts(message, language):
    import gtts
    gTTS = gtts.gTTS
    # Map the language names/codes to basic gTTS codes
    lang_map = {
        "en-US": "en",
        "hi-IN": "hi",
        "pa-IN": "pa"
    }
    
    # Default to English if mapping fails
    gtts_lang = lang_map.get(language, "en")
    
    try:
        tts_audio = gTTS(text=message, lang=gtts_lang, slow=False)
        tts_audio.save("output.mp3")
        print('Audio content written to file "output.mp3"')
    except Exception as e:
        print(f"Error generating TTS: {e}")
        # Create a silent audio file as fallback to avoid crashing
        open("output.mp3", 'a').close()
