from gtts import gTTS
from tempfile import NamedTemporaryFile
from pydub import AudioSegment
import speech_recognition as sr

recognizer = sr.Recognizer()

def transcribe_audio(audio):
    fileorig = NamedTemporaryFile()
    fileorig.write(audio.content)
    
    filedest = NamedTemporaryFile()
    AudioSegment.from_ogg(fileorig.name).export(filedest.name, format='wav')
    fileorig.close()

    with sr.AudioFile(filedest) as source:
        audio = recognizer.record(source)
    filedest.close()
    
    # recognize speech using Google Speech Recognition
    try:
        text = recognizer.recognize_google(audio, language="es-ES")
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        print("* [VOICE] Recognized text:", text)
    except:
        text = ""
        print("* [VOICE] Could not recognize the audio")
    
    return text


def synthesize_text(text: str):
    try:
        print("* [VOICE] Transcribing reply:", text)
        tts = gTTS(text, lang='es')

        fp = NamedTemporaryFile()
        tts.write_to_fp(fp)

        fdest = NamedTemporaryFile()

        AudioSegment.from_mp3(fp.name).export(fdest.name, format='ogg', codec="libopus")

        fp.close()
        fdest.seek(0)
        audio = fdest
    except:
        print("* [VOICE] Error in the transcription")
        audio = None
    return audio