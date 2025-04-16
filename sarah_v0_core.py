#import neccessary librabries
import os
import speech_recognition as sr
import pyttsx3
from datetime import date, datetime
import python_weather
import asyncio
        
async def get_weather(city: str) -> str:
    async with python_weather.Client(unit=python_weather.IMPERIAL) as client:
        weather = await client.get(city)
        return f"The current temperature in {city} is {weather.temperature}°F."


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
    sarah_v0_response=[]
    if recognized_text  == 'wake up Sarah':
        sarah_v0_response = 'hi, what a good sleep, how can I help you?'
    elif 'date' in recognized_text:
        sarah_v0_response = f"Today is {date.today().strftime('%B %d, %Y')}"
    elif 'goodbye' in recognized_text:
        sarah_v0_response = 'goodbye, have a nice day'
        sarah_v0 = pyttsx3.init() #Text to speech to say goodbye
        voices = sarah_v0.getProperty('voices') 
        sarah_v0.setProperty('voice', voices[1].id)  
        sarah_v0.say(sarah_v0_response)
        sarah_v0.runAndWait()
        break
    elif 'weather' in recognized_text:
            # Extract city name from recognized text
            if 'in' in recognized_text:
                city = recognized_text.split('in')[-1].strip()
                if city:
                    sarah_v0_response = asyncio.run(get_weather(city))
                else:
                    sarah_v0_response = "Please tell me the name of the city."
            else:
                sarah_v0_response = "Please specify a city for the weather."
    elif 'thank you' in recognized_text:
        sarah_v0_response = "You're welcome, I love to hear more questions"
    else:
        sarah_v0_response = f"Sarah don't understand{recognized_text}, can you say again"

    #Text to speech
    sarah_v0 = pyttsx3.init()
    voices = sarah_v0.getProperty('voices') 
    sarah_v0.setProperty('voice', voices[1].id)  
    sarah_v0.say(sarah_v0_response)
    sarah_v0.runAndWait()

