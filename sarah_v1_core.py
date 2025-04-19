#import neccessary librabries
import os
import speech_recognition as sr
import pyttsx3
import asyncio
import pyjokes
from sarah_module import get_timezone, get_local_time ,get_weather


while True:
    #Speech recognition
    r = sr.Recognizer()
    with sr.Microphone() as user:
        print("...")
        audio = r.listen(user)
    try:
        recognized_text = r.recognize_google(audio)
    except sr.UnknownValueError:
        print("")
    except sr.RequestError as e:
        recognized_text = "Sarah could not request results from server, please try again"
    print('Thinking...')

    #Sarah_v0_brain
    sarah_v1_response=[]
    if recognized_text  == 'wake up Sarah':
        sarah_v1_response = 'hi, what a good sleep, how can I help you?'
    elif 'time' in recognized_text or 'date' in recognized_text:
        if 'in' in recognized_text:
            city = recognized_text.split('in')[-1].strip()
            try:
                time, date_today = get_local_time(city)
                if 'time' in recognized_text:
                    sarah_v1_response = f"The current time in {city} is {time}"
                elif 'date' in recognized_text:
                    sarah_v1_response = f"Today in {city} is {date_today}"
            except:
                sarah_v1_response = "Sorry, I couldn't find that city. Please try again."
        else:
            sarah_v1_response = "Please specify a city for the time or date."
    elif 'goodbye' in recognized_text:
        sarah_v1_response = 'goodbye, have a nice day'
        sarah_v1 = pyttsx3.init() #Text to speech to say goodbye
        voices = sarah_v1.getProperty('voices') 
        sarah_v1.setProperty('voice', voices[1].id)  
        sarah_v1.say(sarah_v1_response)
        sarah_v1.runAndWait()
        break
    elif 'weather' in recognized_text:
            # Extract city name from recognized text
            if 'in' in recognized_text:
                city = recognized_text.split('in')[-1].strip()
                if city:
                    sarah_v1_response = asyncio.run(get_weather(city))
                else:
                    sarah_v1_response = "Please tell me the name of the city."
            else:
                sarah_v1_response = "Please specify a city for the weather."
    elif 'joke' in recognized_text:
        sarah_v1_response = pyjokes.get_joke()
    elif 'thank you' in recognized_text:
        sarah_v1_response = "You're welcome, I love to hear more questions"
    else:
        sarah_v1_response = f"Sarah don't understand{recognized_text}, can you say again"

    #Text to speech
    sarah_v1 = pyttsx3.init()
    voices = sarah_v1.getProperty('voices') 
    sarah_v1.setProperty('voice', voices[1].id)  
    sarah_v1.say(sarah_v1_response)
    sarah_v1.runAndWait()

