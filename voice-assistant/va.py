import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import time
import subprocess
import wolframalpha
import requests
import cv2
import pyautogui
from pprint import pprint

engine = pyttsx3.init()
engine.setProperty('rate', 150)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


def speak(text):
    engine.say(text)
    engine.runAndWait()
    # engine.stop()


def take_command():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)

        try:
            cm = r.recognize_google(audio, language="en-US")
            print(f"you said: {cm}\n")

        except:
            print("Sorry, I didn't understand, please say it again.\n")
            speak("Sorry, I didn't understand, please say it again.")
            return "None"
    return cm


NAME = "Reza"


def welcome():
    hour = datetime.datetime.now().hour
    if 0 <= hour <= 12:
        print("Hello, Good Morning.\n")
        speak("Hello, Good Morning.")
    elif 12 <= hour <= 16:
        print("Hello, Good Afternoon.\n")
        speak("Hello, Good Afternoon.")
    else:
        print("Hello, Good Evening.\n")
        speak("Hello, Good Evening.")

    print("What is your name?\n")
    speak("What is your name?")
    global NAME
    while True:
        NAME = take_command().lower()
        if NAME != "none":
            break
    print(f"Welcome {NAME}. lets start!\n")
    speak(f"Welcome {NAME}. lets start!")


welcome()
while True:
    print("How can I help you?\n")
    speak("How can I help you?")
    command = take_command().lower()

    if "bye" in command or "stop" in command:
        print(f"Goodbye {NAME}\n")
        speak(f"Goodbye {NAME}")
        break

    if "wikipedia" in command:
        print("Searching Wikipedia...\n")
        speak("Searching Wikipedia...")
        command = command.replace("wikipedia", "")
        print("How many sentences of the results would you like to read to you?\n")
        speak("How many sentences of the results would you like to read to you?")
        try:
            sentence = int(take_command())
        except:
            sentence = 3
        result = wikipedia.summary(command, sentences=sentence)
        print(f"{sentence} sentences of your search result in Wikipedia:\n")
        speak(f"{sentence} sentences of your search result in Wikipedia:")
        pprint(result+"\n")
        speak(result)
    elif "youtube" in command:
        webbrowser.open_new_tab("https://www.youtube.com")
        print("Opening YouTube.\n")
        speak("Opening YouTube.")
        time.sleep(5)
    elif "google" in command:
        webbrowser.open_new_tab("https://www.google.com")
        print("Opening Google.\n")
        speak("Opening Google.")
        time.sleep(5)
    elif "gmail" in command:
        webbrowser.open_new_tab("https://www.gmail.com")
        print("Opening Gmail.\n")
        speak("Opening Gmail.")
        time.sleep(5)

    elif "market" in command:
        webbrowser.open_new_tab("https://www.toinfshop.com")
        print("Opening toinfshop.\n")
        speak("Opening toinfshop.")
        time.sleep(5)

    elif "news" in command:
        webbrowser.open_new_tab("https://news.google.com")
        print("Opening news.\n")
        speak("Opening news.")
        time.sleep(5)
    elif "time" in command:
        str_time = datetime.datetime.now().strftime("%H:%M:%S")
        print(str_time+"\n")
        speak(f"the time is {str_time}")
    elif "camera" in command or "photo" in command:
        camera = cv2.VideoCapture(0)
        ret, frame = camera.read()
        if ret:
            cv2.imwrite("your_photo.png", frame)
        camera.release()
        cv2.destroyAllWindows()
        print("Your photo was taken.\n")
        speak("Your photo was taken.")
    elif "screenshot" in command:
        my_screenshot = pyautogui.screenshot()
        my_screenshot.save("screenshot.png")
        print("Your Screenshot was taken.\n")
        speak("Your Screenshot was taken.")
    elif "search" in command:
        command = command.replace("search", "")
        print(f"Searching {command}\n")
        speak(f"Searching {command}")
        webbrowser.open_new_tab(command)
        time.sleep(5)
    elif "question" in command:
        print("Now I can answer your calculation and geography questions.\n")
        speak("Now I can answer your calculation and geography questions.")
        question = take_command()
        app_id = "X7RHRG-4JVEER92T2"
        client = wolframalpha.Client(app_id)
        res = client.query(question)
        answer = next(res.results).text
        print(answer+"\n")
        speak(answer)

    elif "who" in command:
        print("Hello. I am version 1 of the voice assistant and was programmed by Reza.\n")
        speak("Hello. I am version 1 of the voice assistant and was programmed by Reza.")

    elif "write note" in command:
        print(f"What should i write {NAME}?\n")
        speak(f"What should i write {NAME}?")
        note = take_command()
        print(f"{NAME}, should I include time?\n")
        speak(f"{NAME}, should I include time?")
        ans = take_command()
        if "y" in ans:
            str_time = datetime.datetime.now().strftime("%H:%M:%S")
            with open("note.txt", "w") as file:
                file.write(str_time + "\n")
                file.write("-" * 40 + "\n")
                file.write(note)
        else:
            with open("note.txt", "w") as file:
                file.write(note)
    elif "show note" in command:
        print("Showing Notes:\n")
        speak("Showing Notes:")
        with open("note.txt", "r") as file:
            s = file.read()
            print(s + "\n")
            speak(s)
    elif "telegram" in command:
        print("Opening Telegram!\n")
        speak("Opening Telegram!")
        os.startfile(r"C:\Users\User\AppData\Roaming\Telegram Desktop\Telegram.exe")
        time.sleep(5)
    elif "logout" in command:
        print("Your system will log out after 5 seconds!\n")
        speak("Your system will log out after 5 seconds!")
        time.sleep(5)
        subprocess.call(["shutdown", "/l "])
    elif "weather" in command:
        api_key = "10e2d0da35d4e43c6f3d7675bc203348"
        base_url = "https://api.openweathermap.org/data/2.5/weather?"
        print("What is the city name?\n")
        speak("What is the city name?")
        city_name = take_command()
        complete_url = base_url + "appid=" + api_key + "&q=" + city_name
        response = requests.get(complete_url)
        res = response.json()
        if res["cod"] != "404":
            main = res["main"]
            temperature = main["temp"]
            humidity = main["humidity"]
            weather = res["weather"]
            weather_description = weather[0]["description"]
            print(f"temperature in kelvin unit = {temperature}\n")
            speak(f"temperature in kelvin unit = {temperature}")
            print(f"humidity = {humidity}\n")
            speak(f"humidity = {humidity}")
            print(f"weather description = {weather_description}\n")
            speak(f"weather description = {weather_description}")