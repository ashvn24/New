
# import modules
import base64
import openai
import subprocess  # subprocess module allows you to spawn new processes
from datetime import datetime
# master
import pyjokes  # for generating random jokes
import requests
import json
from PIL import Image, ImageGrab
from gtts import gTTS

# for 30 seconds clip "Jarvis, clip that!" and discord ctrl+k quick-move (might not come to fruition)
from pynput import keyboard
from pynput.keyboard import Key, Listener
from pynput.mouse import Button, Controller

# =======
from playsound3 import playsound  # for sound output

# master
# auto install for pyttsx3 and speechRecognition
import os
try:
    import pyttsx3  # Check if already installed
except:  # If not installed give exception
    os.system('pip install pyttsx3')  # install at run time
    import pyttsx3  # import again for speak function

try:
    import speech_recognition as sr
except:
    os.system('pip install speechRecognition')
    # speech_recognition Library for performing speech recognition with support for Google Speech Recognition, etc..
    import speech_recognition as sr

# importing the pyttsx3 library
import webbrowser
import smtplib

# initialisation
engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
engine.setProperty("rate", 150)
exit_jarvis = False


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def listen_for_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)

    try:
        command = r.recognize_google(audio).lower()
        print(f"You said: {command}")
        return command
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print(f"Error: {e}")


def speak_news():
    url = "http://newsapi.org/v2/top-headlines?sources=the-times-of-india&apiKey=049055d21ef24698817d7601b26f5eda"
    news = requests.get(url).text
    news_dict = json.loads(news)
    arts = news_dict["articles"]
    speak("Source: The Times Of India")
    speak("Todays Headlines are..")
    for index, articles in enumerate(arts):
        speak(articles["title"])
        if listen_for_command() == "enough":
            print("Exiting news headlines...")
            break
        if index == len(arts) - 1:
            break
        speak("Moving on to the next news headline...")
    speak("These were the top headlines, Have a nice day Sir!!")


def sendEmail(to, content):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login("ashwinvk77@gmail.com", "ktsg khti mimn zphi")
    server.sendmail("ashwinvk77@gmail.com", to, content)
    server.close()


# stab = (base64.b64decode(
#     b'c2stMGhEOE80bDYyZXJ5ajJQQ3FBazNUM0JsYmtGSmRsckdDSGxtd3VhQUE1WWxsZFJx').decode("utf-8"))
# api_key = stab


def ask_gpt3(que):
    try:
        openai.api_key = 'sk-proj-G4XDc3VC3e3hv8ooaNGLT3BlbkFJKRgTm00kRblD40fhFsRS'
        response = openai.Completion.create(
            model="gpt-3.5-turbo",
            messages=f"Answer the following question: {que}\n",
            max_tokens=150,
            n=1,
            stop=None,
            stream=True,
            temperature=0.7
        )
        answer = response.choices[0].text.strip()
        return answer
    except openai.error.RateLimitError as e:
        speak(f"sorry, your limit reached for today")
        return

def wishme():
    # This function wishes user
    hour = int(datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning!")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I m Jarvis  ! how can I help you sir")


# obtain audio from the microphone
def takecommand():
    # it takes user's command and returns string output
    wishme()
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.dynamic_energy_threshold = 500
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-in")
        print(f"User said {query}\n")
    except Exception as e:
        speak("Sorry, I didn't catch you")
        query = takecommand()
    return query


# for audio output instead of print
def voice(p):
    myobj = gTTS(text=p, lang="en", slow=False)
    myobj.save("try.mp3")
    playsound("try.mp3")


# recognize speech using Google Speech Recognition


def on_press(key):
    if key == keyboard.Key.esc:
        return False  # stop listener
    try:
        k = key.char  # single-char keys
    except:
        k = key.name  # other keys
    if k in ["1", "2", "left", "right"]:  # keys of interest
        # self.keys.append(k)  # store it in global-like variable
        print("Key pressed: " + k)
        return False  # stop listener; remove this if want more keys


# Run Application with Voice Command Function
# only_jarvis
def on_release(key):
    print("{0} release".format(key))
    if key == Key.esc():
        # Stop listener
        return False
    


def get_app(Q):
    current = Controller()
    # master
    if Q == "time":
        print(datetime.now())
        x = datetime.now()
        voice(x)
    elif Q == "what's today's news":
        speak_news()

    elif Q == "open notepad":
        subprocess.call(["Notepad.exe"])
    elif Q == "open calculator":
        subprocess.call(["calc.exe"])
    elif Q == "open stikynot":
        subprocess.call(["StikyNot.exe"])
    elif Q == "open shell":
        subprocess.call(["powershell.exe"])
    elif Q == "open paint":
        subprocess.call(["mspaint.exe"])
    elif Q == "open cmd":
        subprocess.call(["cmd.exe"])
    elif Q == "open discord":
        subprocess.call(["discord.exe"])
    elif Q == "open browser":
        subprocess.call(["C:\\Program Files\\Internet Explorer\\iexplore.exe"])
    elif Q == "open vs code":
        subprocess.call(["C:\\Program Files\\Internet Explorer\\iexplore.exe"])
    # patch-1
    elif Q == "open youtube":
        webbrowser.open("https://www.youtube.com/")  # open youtube
    elif Q == "open google":
        webbrowser.open("https://www.google.com/")  # open google
    elif Q == "open github":
        webbrowser.open("https://github.com/")
    elif Q == "search for":
        que = Q.lstrip("search for")
        answer = ask_gpt3(que)

    elif (
        Q == "send mail"
    ):  # here you want to change and input your mail and password whenver you implement
        try:
            speak("What should I say?")
            r = sr.Recognizer()
            with sr.Microphone() as source:
                print("Listening...")
                r.pause_threshold = 1
                content = r.listen(source)
            speak("to whom should i mail?")
            r = sr.Recognizer()
            with sr.Microphone() as source:
                print("Listening...")
                r.pause_threshold = 1
                to = r.listen(source)
            # content = input("Enter content")
            sendEmail(to, content)
            speak("Email has been sent!")
        except Exception as e:
            print(e)
            speak("Sorry, I can't send the email.")
    # =======
    #   master
    
    elif Q == "take screenshot":
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        
        snapshot = ImageGrab.grab()
        folder_name = r"downloaded-files"
        folder_time = datetime.now().strftime("%Y-%m-%d_%I-%M-%S_%p")
        extention = ".jpg"
        folder_to_save_files = folder_name + folder_time + extention
        folder_path = os.path.join(desktop_path, folder_name)
        os.makedirs(folder_path, exist_ok=True)

        # Save the screenshot to the "downloaded-files" folder
        file_path = os.path.join(folder_path, folder_to_save_files)
        snapshot.save(file_path)
        speak("screen shot saved")

    elif Q == "Jokes":
        speak(pyjokes.get_joke())

    elif Q == "start recording":
        current.add("Win", "Alt", "r")
        speak("Started recording. just say stop recording to stop.")

    elif Q == "stop recording":
        current.add("Win", "Alt", "r")
        speak("Stopped recording. check your game bar folder for the video")

    elif Q == "clip that":
        current.add("Win", "Alt", "g")
        speak("Clipped. check you game bar file for the video")
        with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()
    elif Q == "take a break":
        speak("Thank you")
        exit()
    else:
        answer = ask_gpt3(Q)

 


# Call get_app(Query) Func.

if __name__ == "__main__":
    while not exit_jarvis:
        Query = takecommand().lower()
        get_app(Query)
    exit_jarvis = True
