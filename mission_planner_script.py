import time

neutral = True
first = True
def speech_commands(filename):
	Script.SendRC(3,950,True)
	global neutral
	global first
	with open(filename, 'r') as f:	
		command = f.readline()
		if command == "on":
			if first == True:
				MAV.doARM(True)
				first = False
			Script.SendRC(3,1010,True)
		elif command == "off":
			Script.SendRC(3,900,True)
			MAV.doARM(False)
	neutral = False
def motion_commands(filename):
	global neutral
	with open(filename, 'r') as f:
		command = f.readline()
		if command == "up":
			Script.SendRC(3,1150,True)
			neutral = False
		elif command == "neutral":
			Script.SendRC(3,1100,True)
			neutral = True
		elif command == "down":
			Script.SendRC(3,1030,True)
			neutral = False
with open("C:\Users\user-zaki\Documents\Capstone\speech_commands.txt", 'w'):
	pass
with open("C:\Users\user-zaki\Documents\Capstone\motion_commands.txt", 'w'):
	pass
while True:
	if neutral == True:
		speech_commands("C:\Users\user-zaki\Documents\Capstone\speech_commands.txt")
	else:
		motion_commands("C:\Users\user-zaki\Documents\Capstone\motion_commands.txt")

