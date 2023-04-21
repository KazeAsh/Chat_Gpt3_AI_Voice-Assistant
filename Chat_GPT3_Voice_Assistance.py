import openai
import pyttsx3
import speech_recognition as sr
import time

#OpenAI API Key
openai.api_key = "sk-R3WBqsFvjnCgJvYJSoRNT3"#Example

#Initialize the text-to-speech engine
engine = pyttsx3.init()

def transcribe_audio_to_text(filename):
    recongizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recongizer.record(source)
    try:
        return recongizer.recognize_google(audio)
    except:
         print('Skipping unknown error')

#Generate Response on given prompt
def generate_response(prompt):
    response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=4000,
            n=1,
            stop=None,
            temperature=0.5,
     )
    return response["choices"][0]["text"]

def speak_text(text):
    engine.say(text)
    engine.runAndWait()

def main():
    while True:
        #wait for user to say 'Genius'
        print("Say 'Genius' to start recording your question.")
        with sr.Microphone() as source:
            recognizer = sr.Recognizer()
            audio = recognizer.listen(source)
            try:
                transcription = recognizer.recognize_google(audio)
                if transcription.lower() == "genius":
                    #record audio
                    filename = "input.wav"
                    print ("Say your question.")
                    with sr.Microphone() as source:
                        recognizer = sr.Recognizer()
                        source.pause_threshold = 1
                        audio = recognizer.listen(source, phrase_time_limit=None, timeout=None)
                        with open(filename, "wb") as f:
                            f.write(audio.get_wav_data())
                    #Transcribe audio to text
                    text = transcribe_audio_to_text(filename)
                    if text:
                        print(f"You said: {response}")

                        #Generate Reponse using GPT-3
                        response = generate_response(text)
                        print(f"GPT-3 says: {response}")
                        #Read reponse using text-to-speech
                        speak_text(response)
            except Exception as e:
                    print("An error occured: {}".format(e))
if __name__ == "__Main__":
    main()      