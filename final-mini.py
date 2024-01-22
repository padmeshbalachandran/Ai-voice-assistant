import speech_recognition as sr
import openai
import pyttsx3
import time
import subprocess
import wikipedia
import webbrowser
import datetime
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from langdetect import detect
import pyaudio

# Set up OpenAI credentials
openai.api_key = "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"

# Define language model ID
model_id = "text-davinci-003"

# Initialize PyAudio for microphone input
pa = pyaudio.PyAudio()
stream = pa.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)

# Initialize speech recognition
r = sr.Recognizer()


def text_to_speech(txt):
    engine = pyttsx3.init("sapi5")
    voices = engine.getProperty("voices")
    engine.setProperty('voice', voices[1].id)
    engine.say(txt)
    engine.runAndWait()


def translate_to_language(text, language):
    model = f"text-{language}"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Translate the following English text to {language}: \n{text}\n\nTranslation:",
        max_tokens=1024,
        temperature=0.5,
        n=1,
        stop=None,
       # model=model
    )
    translation = response.choices[0].text.strip()
    return translation


def generate_response(prompt):
    completions = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
        stop=None,
        temperature=0.9,
    )

    message = completions.choices[0].text
    return message.strip()


def wishMe():
        hour = datetime.datetime.now().hour
        if hour >= 0 and hour < 12:
            text_to_speech("Hello Sir,Good Morning")
            print("Hello Sir,Good Morning")
        elif hour >= 12 and hour < 18:
            text_to_speech("Hello Sir,Good Afternoon")
            print("Hello Sir,Good Afternoon")
        else:
            text_to_speech("Hello Sir,Good Evening")
            print("Hello Sir,Good Evening")


wishMe()

# Main loop for voice input and OpenAI GPT-3 response
while True:
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        user_input = r.recognize_google(audio, language='es-ES')
        print(f"You: {user_input}\n")

    except Exception as e:
        # print(e)
        print("Sage: Say that again please...")
        text_to_speech("Sorry,can you repeat that again.")

    str(user_input)

    if "Quién eres" in user_input or "quién eres" in user_input:
        response = "Hola, soy Sage. Soy un asistente de voz de IA creado por God Niranjan y equipo para su Mini Proyecto"
        print("Sage : " + response)
        text_to_speech(response)

    elif "bien" in user_input or "Bien" in user_input:
        response = "Ok, ¿cómo puedo ayudarte?"
        print('Sage: ' + response)
        text_to_speech(response)

    elif "wikipedia" in user_input:
        user_input = user_input.replace("wikipedia", "")
        response = wikipedia.summary(user_input, sentences=3)
        text_to_speech("Según Wikipedia")
        print("Sage :  According to Wikipedia" + response)
        text_to_speech(response)

    elif 'hola' in user_input:
        text_to_speech('¡Hola, Sage! ¿Cómo te va el día?')
        print('¡Hola, Sage! ¿Cómo te va el día?')

    elif 'Tu día' in user_input or 'tu día' in user_input:
        text_to_speech('Estoy teniendo un buen día.')
        print('Estoy teniendo un buen día.')

    elif 'buscar' in user_input:
        user_input = user_input.replace("search", "")
        webbrowser.open_new_tab(user_input)
        time.sleep(5)

    elif 'Adiós' in user_input or 'adiós' in user_input:
        text_to_speech('Adiós, apagado del sistema')
        print('Adiós, apagado del sistema')
        break

    elif 'noticia' in user_input:
        news = webbrowser.open_new_tab("https://timesofindia.indiatimes.com/home/headlines")
        print('Aquí hay algunos titulares del Times of India, Feliz lectura..')
        text_to_speech('Aquí hay algunos titulares del Times of India, Feliz lectura')
        time.sleep(6)

    elif 'Hora' in user_input:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        text_to_speech(f"the time is {strTime}")
        print('Sage: ' + strTime)

    elif 'escribir' in user_input or 'codigo' in user_input:
        response = generate_response(user_input)
        translated_response = translate_to_language(response, "Spanish")
        print('Sage: ' + response)

    elif 'morir' in user_input or 'suicidio' in user_input:
        response = "No puedo hacer eso"
        text_to_speech(response)
        print('Sage: ' + response)

    elif 'Soy yo' in user_input or 'soy yo' in user_input:
        response = "Hola, soy Sage."
        text_to_speech(response)
        print('Sage: ' + response)

    elif 'su edad' in user_input:
        response = "No puedo envejecer porque soy una IA."
        text_to_speech(response)
        print('Sage: ' + response)

    else:
        response = generate_response(user_input)
        translated_response = translate_to_language(response, "Spanish")
        print("Sage : " + translated_response)
        text_to_speech(translated_response)