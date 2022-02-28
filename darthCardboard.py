import speech_recognition as sr   # voice recognition library

import random                     
import pyttsx3                    # offline Text to Speech

import datetime                   
import webbrowser                 # to open and perform web tasks

import serial                     # for USB  communication
import pywhatkit                  # for web automation

# Declare robot name (Wake-Up word)
robot_name = 'darth'

# random words list
hi_words = ['hi', 'hello', ]
bye_words = ['bye', ]



engine = pyttsx3.init()                    

listener = sr.Recognizer()                

# Connect to arduino board
try:
    port = serial.Serial("COM3", 9600)
    print("Phycial body, connected.")
except:
    print("Unable to connect to my physical body")


def listen():
	# listen to what user says
	try:
		with sr.Microphone() as source:                         # get input from mic
			print("Talk>>")
			voice = listener.listen(source)                     # listen from microphone
			command = listener.recognize_google(voice).lower()  # use google API
			print(command)

			# look for wake up word in the beginning
			if (command.split(' ')[0] == robot_name):
				# if wake up word found....
				print("[--- Wake up ---]")
				process(command)                 # call process funtion to take action
	except:
		pass

def process(words):
	""" process what user says and take actions """
	print(words) # check if it received any command

	# split by space and ignore the wake-up word
	word_list = words.split(' ')[1:]  

	if (len(word_list)==1):
		if (word_list[0] == robot_name):
			talk("How Can I help you?")
		return

	if word_list[0] == 'play':
		talk("fine, but dont ask again, the emperor is not as forgiving as I")
		extension = ' '.join(word_list[1:])                    
		port.write(b'u')
		pywhatkit.playonyt(extension)   
		port.write(b'l')          
		return

	elif word_list[0] == 'search':
		"""if command for google search"""
		port.write(b'u')
		talk("I find your lack of using google yourself disturbing")
		port.write(b'l')
		extension = ' '.join(word_list[1:])
		pywhatkit.search(extension)
		return


	elif word_list[0] == 'open':
		port.write(b'l')
		talk("I grow weary of these commands")
		url = f"http://{''.join(word_list[1:])}"   # make the URL
		webbrowser.open(url)
		return

	elif word_list[0] == 'dance':
		port.write(b'U')



def talk(sentence):
	engine.say(sentence)
	engine.runAndWait()


while True:
    listen()  

