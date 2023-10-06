
import datetime

import requests
from Models import AssistantModel
import wikipedia
import speech_recognition  as sr
import pyttsx3
base_url = "https://en.wikipedia.org/api/rest_v1"
engine = pyttsx3.init()
# List available voices
voices = engine.getProperty('voices')
engine.setProperty('rate', 150)  # Adjust as needed
engine.setProperty('volume', 1)  # Adjust as needed
engine.setProperty('pitch', 5)  # Adjust as needed
engine.setProperty('language', 'en')
engine.setProperty('voice', voices[1].id)  # Example voice
# import training 
# training.Train()
recognizer = sr.Recognizer()
captured_words = []
topic = 'what is searching'
AssistantName = 'alexa'
jarvis = AssistantModel()
previouscommand = ''
previoustask = ''
def speak(text):
    engine.say(text)
    engine.runAndWait()
    
def performTask(task,topic = None,**kwargs):
    
    Keywordargs =  dict(kwargs.items())
    if task == 'calling':
        text = 'Hi Sir, How can i help you.'
        speak(text)
    if task == 'time':
        
        current_time = datetime.datetime.now()
        hour = current_time.strftime("%I")
        minute = current_time.strftime("%M")
        am_pm = current_time.strftime("%p")

        # Convert hour and minute to words
        hour_words = {
            '01': 'one',
            '02': 'two',
            '03': 'three',
            '04': 'four',
            '05': 'five',
            '06': 'six',
            '07': 'seven',
            '08': 'eight',
            '09': 'nine',
            '10': 'ten',
            '11': 'eleven',
            '12': 'twelve'
        }

        minute_words = {
            '00': '',
            '01': 'one',
            '02': 'two',
            '03': 'three',
            '04': 'four',
            '05': 'five',
            '06': 'six',
            '07': 'seven',
            '08': 'eight',
            '09': 'nine',
            '10': 'ten',
            '11': 'eleven',
            '12': 'twelve',
            '13': 'thirteen',
            '14': 'fourteen',
            '15': 'fifteen',
            '16': 'sixteen',
            '17': 'seventeen',
            '18': 'eighteen',
            '19': 'nineteen',
            '20': 'twenty',
            '21': 'twenty-one',
            '22': 'twenty-two',
            '23': 'twenty-three',
            '24': 'twenty-four',
            '25': 'twenty-five',
            '26': 'twenty-six',
            '27': 'twenty-seven',
            '28': 'twenty-eight',
            '29': 'twenty-nine',
            '30': 'thirty',
            '31': 'thirty-one',
            '32': 'thirty-two',
            '33': 'thirty-three',
            '34': 'thirty-four',
            '35': 'thirty-five',
            '36': 'thirty-six',
            '37': 'thirty-seven',
            '38': 'thirty-eight',
            '39': 'thirty-nine',
            '40': 'forty',
            '41': 'forty-one',
            '42': 'forty-two',
            '43': 'forty-three',
            '44': 'forty-four',
            '45': 'forty-five',
            '46': 'forty-six',
            '47': 'forty-seven',
            '48': 'forty-eight',
            '49': 'forty-nine',
            '50': 'fifty',
            '51': 'fifty-one',
            '52': 'fifty-two',
            '53': 'fifty-three',
            '54': 'fifty-four',
            '55': 'fifty-five',
            '56': 'fifty-six',
            '57': 'fifty-seven',
            '58': 'fifty-eight',
            '59': 'fifty-nine',
        }
        text = f'its {hour_words[hour]} {minute_words[minute]}'
        speak(text)
    if task == 'train':
        print(Keywordargs)
        jarvis.updateData(command = Keywordargs['command'],task = Keywordargs['todo'])
        jarvis.Train()

    elif task == 'lights on':
        text = 'turning the light on'
        speak(text)
        
    elif task == 'lights off':
        text = 'turning the light off'
        speak(text)
    
    elif task == 'search':
        print('searching...')
        # Create a Wikipedia API object
        
        # print('searchin for ',topic)# You can specify the language (e.g., 'en' for English)
        if topic is not None:
            try:
                text  = wikipedia.summary(topic)
                text  = str(text).split('. ')
                text = text[:3]
                text = '. '.join(text)
                print(text)
                speak(text)
            except:
                text = 'please mention the exact topic'
                speak(text)
        
    else:
        print('no task assigned')
   
def capture_words():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=2)
        print("Listening... (Press Ctrl+C to stop)")
        try:
            while True:
                # print(captured_words)
                audio_chunk = recognizer.listen(source,phrase_time_limit=3)
                try:
                    text = recognizer.recognize_google(audio_chunk)
                    text = text.lower()
                    print('you said' ,text)
                    if str(text).strip() == 'correct':
                        jarvis.updateData(command=previouscommand, task=previoustask)
                        print('updated')
                        jarvis.Train()
                        print('Trained')
                    
                    if AssistantName in text:
                        command = str(text).replace(AssistantName,'').strip()
                        if command == '':
                            command = 'calling'
                        # print('command','--'+command+'--')
                        task = jarvis.Command(command)
                        previouscommand = command
                        previoustask = task
                        print(task)
                        if task == 'search':
                            topic = str(command).replace('search','')
                            performTask('search',topic = topic)
                            continue 
                        performTask(task)     
                        speak('Was that corrent')                  
                    else:
                        pass
                except sr.UnknownValueError:
                    pass 
                # Ignore audio chunks that couldn't be recognized
        except KeyboardInterrupt:
            print("Listening stopped.")
            
capture_words()

