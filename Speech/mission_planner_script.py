import time

def speech_commands(filename):
	while True:
		with open(filename, 'r') as f:
			if f.readline() == "on":
				MAV.doARM(True)
			elif f.readline() == "off":
				MAV.doARM(False)
			time.sleep(2)
def motion_commands(filename):
	Script.SendRC(3,950,True)
	MAV.doARM(True)
	while True:
		with open(filename, 'r') as f:
			if f.readline() == "up":
				Script.SendRC(3,1100,True)
			elif f.readline() == "neutral":
				Script.SendRC(3,1000,True)
			elif f.readline() == "down":
				MAV.doARM(False)
motion_commands("C:\Users\user-zaki\Documents\KinectSamplesBeta\Managed\Speech\out.txt")