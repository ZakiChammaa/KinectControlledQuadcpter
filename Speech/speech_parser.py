from subprocess import Popen, PIPE, STDOUT
import sys

def parse_speech(filename):
	p = Popen(filename, stdout=PIPE, bufsize=1)
	for line in iter(p.stdout.readline, b''):
		if 'Recognized' in line:
			# print cs.armed
			# MAV.doARM(True)
			# Script.Sleep(5000)
			# print cs.armed
			print "on nigga"
		print line,
	p.stdout.close()
	p.wait()
def process_motion(filename):
	p = Popen(filename, stdout=PIPE, bufsize=1)
	for line in iter(p.stdout.readline, b''):
		# X coordinate
		if line.split[0] > 0:
			# move right
			print 'right'
		else:
			# move left
			print 'left'
		# Y coordinate
		if line.split[1] > 0:
			# move up
			print 'up'
		else:
			# move down
			print 'down'
		# Z coordinate
		if line.split[2] > 0:
			# move forward
			print 'forward'
		else:
			# move backward
			print 'backward'
	p.stdout.close()
	p.wait()

parse_speech('C:\Users\user-zaki\Documents\KinectSamplesBeta\Managed\Speech\Bin\Debug\Speech.exe')