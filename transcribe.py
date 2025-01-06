import speech_recognition as sr
from pydub import AudioSegment

# Convert MP3 file to WAV and adjust settings
sound = AudioSegment.from_mp3("F:\\NVideos\\Desktop\\interviu.mp3")
sound = sound.set_frame_rate(16000).set_channels(1)  # Ensure proper format
sound.export("interviu_converted.wav", format="wav")

# Initialize the recognizer
r = sr.Recognizer()

# Load the audio file
with sr.AudioFile("interviu_converted.wav") as source:
    audio_data = r.record(source)  # Load audio to memory

    # Perform speech recognition
    try:
        text = r.recognize_google(audio_data, language='lt-LT')
        print("Transcription: ", text)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")