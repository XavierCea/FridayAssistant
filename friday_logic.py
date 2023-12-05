import speech_recognition as sr
import subprocess as sp
import threading as tr
import pyttsx3, pywhatkit, wikipedia, datetime, keyboard, os, colors, weather
from pygame import mixer



NAME = "friday"
NOTE = "C:/Users/xavie/nota.txt"
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

def yt_reproduce(recognize):
    """Recognizes the name of the song that the user wants to listen to and searches on YouTube to play it"""
    music = recognize.replace('reproduce', '')
    print("Reproduce "+ music)
    talk("Reproduciendo "+ music)
    pywhatkit.playonyt(music)
    
def wiki_search(recognize):
    """Recognizes what the user needs to search for, giving the first line of Wikipedia about it."""
    search = recognize.replace('busca', '')
    wikipedia.set_lang("es")
    wiki = wikipedia.summary(search, 1)
    print(search + ": "+ wiki)
    talk(wiki)

def set_alarm(recognize):
    """Recognizes the time at which the user wants to set an alarm, causing it to ring at the agreed time."""
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

def open(recognize):
    """Opens a previously saved program or web page that the user wants quick access to"""
    for site in sites:
        if site in recognize:
            sp.call(f'start chrome.exe {sites[site]}', shell=True)
            talk(f'Abriendo {site}')
    for program in programs:
        if program in recognize:
            os.startfile(programs[program])
            talk(f'Abriendo {program}')

def file_open(recognize):
    """Open a file that the user has linked with quick access"""
    for file in files:
        if file in recognize:
            sp.Popen([files[file]], shell=True)
            talk(f'Abriendo {file}')

def run_friday():
    """Runs the friday algorithm and recognize the voice input option to realize the different actions"""
    recognize = listen()
    if 'reproduce' in recognize:
        yt_reproduce(recognize)
    elif 'busca' in recognize:
        wiki_search(recognize)
    elif 'alarma' in recognize:
        set_alarm(recognize)
    elif 'colores' in recognize:
        talk("Enseguida")
        colors.capture()
    elif 'abre' in recognize:
        open(recognize)
    elif 'archivo' in recognize:
        file_open(recognize)
    elif 'escribe' in recognize:
        try:
            with open(NOTE, 'a') as f:
                write(f)
        except FileNotFoundError as e:
            file = open(NOTE, 'w')
            write(f)
    elif 'tiempo' in recognize:
        print(recognize)            
        locate = recognize.replace('tiempo', '')
        weather.weather(locate)
    else:
        talk('Comando invalido') 
        print('Comando invalido')            
                   