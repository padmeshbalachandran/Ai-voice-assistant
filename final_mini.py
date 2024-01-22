import speech_recognition as sr
import openai
import pyttsx3
import time
import pyaudio
import subprocess
import wikipedia
import webbrowser
import datetime
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from langdetect import detect


def detect_language(text):
    lang = detect(text)
    return lang


openai.api_key = "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"


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


def text_to_speech(text):
    engine = pyttsx3.init("sapi5")
    voices = engine.getProperty("voices")
    engine.setProperty('voice', voices[1].id)
    engine.say(text)
    engine.runAndWait()


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

while True:
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        user_input = r.recognize_google(audio, language='en-in')
        print(f"You: {user_input}\n")

    except Exception as e:
        # print(e)
        print("Sage: Say that again please...")
        text_to_speech("Sorry,can you repeat that again.")

    la = detect_language(user_input)
#    print(la)
# '''-------------------------------------English--------------------------------------------------------'''

    if "Who are you" in user_input or "who are you" in user_input:
            response = "Hello, I am Sage. I am an AI voice assistant created by God Niranjan and team for their Mini Project"
            print("Sage : " + response)
            text_to_speech(response)

    elif "fine" in user_input or "Fine" in user_input:
            response = "Ok, How may I help you?"
            print('Sage: ' + response)
            text_to_speech(response)

    elif "wikipedia" in user_input:
            user_input = user_input.replace("wikipedia", "")
            response = wikipedia.summary(user_input, sentences=3)
            text_to_speech("According to Wikipedia")
            print("Sage :  According to Wikipedia" + response)
            text_to_speech(response)

    elif 'hello' in user_input or 'hi' in user_input:
            text_to_speech('Hi, I am Sage. How is your day?')
            print('Hi, I am Sage.')

    elif 'your day' in user_input or 'Your Day' in user_input:
            text_to_speech('I am having a good day.')
            print('I am having a good day.')

    elif 'search' in user_input:
            user_input = user_input.replace("search", "")
            webbrowser.open_new_tab(user_input)
            time.sleep(5)

    elif 'bye' in user_input or 'goodbye' in user_input or 'shutdown' in user_input:
            text_to_speech('Bye, Have a good Day, system shutting down')
            print('Shutting down,Good bye')
            break

    elif 'news' in user_input:
            news = webbrowser.open_new_tab("https://timesofindia.indiatimes.com/home/headlines")
            print('Here are some headlines from the Times of India,Happy reading..')
            text_to_speech('Here are some headlines from the Times of India,Happy reading')
            time.sleep(6)

    elif 'time' in user_input:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            text_to_speech(f"the time is {strTime}")
            print('Sage: ' + strTime)

    elif 'write' in user_input or 'code' in user_input:
            response = generate_response(user_input)
            print('Sage: ' + response)

    elif 'die' in user_input or 'suicide' in user_input:
            response = "I am unable to do that"
            text_to_speech(response)
            print('Sage: ' + response)

    elif 'I am' in user_input or 'i am' in user_input:
            response = "Hello, I am Sage."
            text_to_speech(response)
            print('Sage: ' + response)

    elif 'your age' in user_input:
            response = "I am unable to age as I am an AI."
            text_to_speech(response)
            print('Sage: ' + response)

    elif 'open spotify' in user_input:
        # Set up Spotify API credentials
        scope = 'user-read-playback-state,user-modify-playback-state'
        client_id = "96021c82ab69465aa3d4642ac1e540c5"
        client_secret = "67cc89878db645838893bdfca5b12d65"
        redirect_uri = "https://open.spotify.com/"
        # Authenticate user and get Spotify access token
        sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri,
                                      scope=scope))

        # Search for the song or playlist you want to play
        playback_type = input("Would you like to play a song or a playlist? ")
        if playback_type == "song":
            song_name = input("What song would you like to play? ")
            results = sp.search(q=song_name, type='track', limit=1)
            uri = results['tracks']['items'][0]['uri']
        elif playback_type == "playlist":
            playlist_name = input("What playlist would you like to play? ")
            playlists = sp.user_playlists('your_spotify_username')
            for playlist in playlists['items']:
                if playlist['name'] == playlist_name:
                    uri = playlist['uri']
                    break

        # Start playback of the song or playlist
        sp.start_playback(context_uri=uri)

    elif 'how are you' in user_input:
        response = "I am fine, how is your day."
        print("Sage : " + response)
        text_to_speech(response)
    else:
            response = generate_response(user_input)
            print("Sage : " + response)
            text_to_speech(response)

# '''-------------------------------------Spanish--------------------------------------------------------'''
