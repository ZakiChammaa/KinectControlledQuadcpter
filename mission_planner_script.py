import time

first_on = True
first_drop = True
first_land = True
first_off = True
first_manual = True
speech_file = "speech_commands.txt"
motion_file = "motion_commands.txt"

with open(speech_file, 'w'):
	pass
with open(motion_file, 'w'):
	pass

def run_speech_commands(input_file):
	global first_on, first_drop, first_land, first_off, first_manual
	with open(speech_file, 'r') as f:	
		speech_command = f.read()
		if speech_command == "activate":
			if first_on == True:
				Script.ChangeMode("Stabilize")
				MAV.doARM(True)
				first_on = False
				Script.Sleep(1500)
				Script.SendRC(4,1500,True)
		elif speech_command == "off":
			if first_off == True:
				MAV.doARM(False)
				Script.SendRC(4,1500,True)
				first_off = False
		elif speech_command == "open":
			if first_drop == True:
				Script.SendRC(6,1350, True)
				first_drop = False
		elif speech_command == "land":
			if first_land == True:
				Script.ChangeMode("Land")
				first_land = False
		elif speech_command == "hold":
			Script.ChangeMode("AltHold")
		elif speech_command == "stabilize":
			Script.ChangeMode("Stabilize")
		elif speech_command == "manual":
			if first_manual == True:
				for i in range(1, 9):
					Script.SendRC(i, 0, True)
				Script.ChangeMode("Stabilize")
				first_manual = False
		print speech_command

def run_motion_commands(input_file):
	with open(motion_file, 'r') as f:
		motion_command = f.readline()
		if motion_command == "up":
			Script.SendRC(3,1150,True) # throttle up
		elif motion_command == "down":
			Script.SendRC(3,982,True)  # zero throttle
		elif motion_command == "right":
			Script.SendRC(1,1580,True) # roll right
		elif motion_command == "left":
			Script.SendRC(1,1420,True) # roll left
		elif motion_command == "forward":
			Script.SendRC(2,1420,True) # pitch forward
		elif motion_command == "back":
			Script.SendRC(2,1580,True) # pitch backwards
		elif motion_command == "yaw_right":
			Script.SendRC(4,1580,True) # yaw right
		elif motion_command == "yaw_left":
			Script.SendRC(4,1420,True) # yaw left
		elif motion_command == "neutral":
			Script.SendRC(3,1100,True)
			Script.SendRC(1,1494,True) # roll neutral
			Script.SendRC(2,1494,True) # pitch neutral
			Script.SendRC(4,1500,True) # yaw neutral
		print motion_command
lock = True
while True:
	if lock == True:
		run_speech_commands(speech_file)
	else:
		run_motion_commands(motion_file)
	lock = not(lock)
	if first_off == False:
		break