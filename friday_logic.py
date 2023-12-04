import speech_recognition as sr
import subprocess as sp
import threading as tr
import pyttsx3, pywhatkit, wikipedia, datetime, keyboard, os, colors
from pygame import mixer



NAME = "friday"
NOTE = "C:/Users/xavie/OneDrive/Escritorio/nota.txt"
DESKTOP = "C:/Users/xavie/OneDrive/Escritorio"

sites = {
    'google' : 'google.es',
    'youtube' : 'youtube.es',
    'whatsapp' : 'web.whatsapp.com',
    'telegram' : 'web.telegram.org',
    'linkedin' : 'linkedin.com',
}

files = {
    'prueba' : 'C:/Users/xavie/OneDrive/Escritorio/Pagina 1.png'
}

programs = {
    'word' : r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE",
    'visual studio code' : r"C:\Program Files\Microsoft VS Code\Code.exe",
    'photoshop' : r"C:\Program Files\Adobe\Adobe Photoshop 2020\Photoshop.exe",
}

listener = sr.Recognizer()
engine = pyttsx3.init()

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 150)

def talk(text):
    """Permit the assistant to talk using voice simulation"""
    engine.say(text)
    engine.runAndWait()

def listen():
    """Listen user microphone inout and recognize voice to recieve commands if assistant name
    is correct"""
    try:
        with sr.Microphone() as source:
            print("Listening...")
            talk("Escuchando...")

            listen = listener.listen(source)
            recognize = listener.recognize_google(listen, language="es")
            recognize = recognize.lower()
            if NAME in recognize:
                recognize = recognize.replace(NAME, '')
    except:
        pass
    return recognize

def write(f):
    """Open a text file with write or create permissions and transcribe the voice recognition to
    write a new text line"""
    talk("¿Qué quieres que escriba?")
    recognize = listen()
    f.write(recognize + os.linesep)
    f.close()
    talk("Listo, puedes revisarlo")
    sp.Popen(NOTE, shell=True)

def run_friday():
    recognize = listen()
    if 'reproduce' in recognize:
        music = recognize.replace('reproduce', '')
        print("Reproduce "+ music)
        talk("Reproduciendo "+ music)
        pywhatkit.playonyt(music)
    elif 'busca' in recognize:
        search = recognize.replace('busca', '')
        wikipedia.set_lang("es")
        wiki = wikipedia.summary(search, 1)
        print(search + ": "+ wiki)
        talk(wiki)
    elif 'alarma' in recognize:
        alarm = recognize.replace('alarma', '')
        alarm = alarm.strip()
        talk("Alarma activada a las " + alarm + " horas")
        print("Alarma activada a las " + alarm + " horas")
        while True:
            if datetime.datetime.now().strftime("%H:%M") == alarm:
                print("DESPIERTA!")
                mixer.init()
                mixer.music.load("alarm.wav")
                mixer.music.set_volume(100)
                mixer.music.play()
                if keyboard.read_key() == "s":
                    mixer.music.stop()
                    break
    elif 'colores' in recognize:
        talk("Enseguida")
        colors.capture()
    elif 'abre' in recognize:
        for site in sites:
            if site in recognize:
                sp.call(f'start chrome.exe {sites[site]}', shell=True)
                talk(f'Abriendo {site}')
        for program in programs:
            if program in recognize:
                os.startfile(programs[program])
                talk(f'Abriendo {program}')
    elif 'archivo' in recognize:
        for file in files:
            if file in recognize:
                sp.Popen([files[file]], shell=True)
                talk(f'Abriendo {file}')
    elif 'escribe' in recognize:
        try:
            with open(NOTE, 'a') as f:
                write(f)
        except FileNotFoundError as e:
            file = open(NOTE, 'w')
            write(f)