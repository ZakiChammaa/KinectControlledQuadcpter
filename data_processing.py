import os
import time
from subprocess import Popen, PIPE, STDOUT
from multiprocessing import Process

# Path to current directory
CURRENT_DIR = os.getcwd()
# Path to motion commands file
OUTPUT_MOTION_FILE_PATH = 'motion_commands.txt'
# Path to speech commands file
OUTPUT_SPEECH_FILE_PATH = 'speech_commands.txt'
# Path to SkeletalViewer.exe
SKELETAL_EXE_PATH = '%s\SkeletalViewer\\bin\Debug\SkeletalViewer.exe' % CURRENT_DIR
# Path to Speech.exe
SPEECH_EXE_PATH = '%s\Speech\Bin\Debug\Speech.exe' % CURRENT_DIR

def process_speech(executable, file_out):
	p = Popen(executable, stdout=PIPE, bufsize=1)
	for line in iter(p.stdout.readline, b''):
		if 'Recognized:on' in line:
			with open(file_out, 'w') as f:		
				f.write("on")
				f.flush()
		elif 'Recognized:off' in line:
			with open(file_out, 'w') as f:		
				f.write("off")
				f.flush()
		print line,
	p.stdout.close()
	p.wait()
def process_motion(executable, file_out):
	first = True
	p = Popen(executable, stdout=PIPE, bufsize=1)
	for line in iter(p.stdout.readline, b''):
		print line,
		if first == True:
			initial_coordinates = [float(i) for i in line.split(',')]
			print initial_coordinates
			first = False
		if float(line.split(",")[1]) > 0.6:	
			with open(file_out, 'w') as f:		
				f.write('up')
				f.flush()
		elif float(line.split(",")[1]) < 0.5 and float(line.split(",")[1]) > 0:  
			with open(file_out, 'w') as f:      	
				f.write('neutral')
				f.flush()
		elif float(line.split(",")[1]) < 0:
			with open(file_out, 'w') as f:
				f.write('down')
				f.flush()
	p.stdout.close()
	p.wait()
if __name__ == '__main__':
	p1 = Process(target = process_motion, args=(SKELETAL_EXE_PATH, OUTPUT_MOTION_FILE_PATH))
	p1.start()
	p2 = Process(target = process_speech, args=(SPEECH_EXE_PATH, OUTPUT_SPEECH_FILE_PATH))
	p2.start()