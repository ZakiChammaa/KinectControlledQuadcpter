import os, sys, time
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

def calibrate(executable, duration):
	endtime = time.time() + duration
	x, y, z = ([] for i in range(3))
	print "calibrating..."
	p = Popen(executable, stdout=PIPE, bufsize=1)
	for line in iter(p.stdout.readline, b''):
		x.append(float(line.split(",")[0]))
		y.append(float(line.split(",")[1]))
		z.append(float(line.split(",")[2]))
		if time.time() >= endtime:
			print "calibration complete"
			p.kill()
			break
	p.stdout.close()
	p.wait()
	return [(min(x), max(x)), (min(y), max(y)), (min(z), max(z))]
def process_speech(executable, file_out):
	p = Popen(executable, stdout=PIPE, bufsize=1)
	for line in iter(p.stdout.readline, b''):
		if 'Recognized:activate' in line:
			with open(file_out, 'w') as f:		
				f.write("activate")
				f.flush()
		elif 'Recognized:off' in line:
			with open(file_out, 'w') as f:		
				f.write("off")
				f.flush()
		elif 'Recognized:open' in line:
			with open(file_out, 'w') as f:		
				f.write("open")
				f.flush()
		elif 'Recognized:land' in line:
			with open(file_out, 'w') as f:		
				f.write("land")
				f.flush()
		elif 'Recognized:hold' in line:
			with open(file_out, 'w') as f:		
				f.write("hold")
				f.flush()
		elif 'Recognized:manual' in line:
			with open(file_out, 'w') as f:		
				f.write("manual")
				f.flush()
		elif 'Recognized:stabilize' in line:
			with open(file_out, 'w') as f:		
				f.write("stabilize")
				f.flush()
		print line,
	p.stdout.close()
	p.wait()
def process_motion(executable, file_out, values):
	n_max_x = ((values[0][1] - values[0][0]) / 2) + values[0][0] + (values[0][1] - values[0][0])*0.35
	n_min_x = ((values[0][1] - values[0][0]) / 2) + values[0][0] - (values[0][1] - values[0][0])*0.35
	n_max_y = ((values[1][1] - values[1][0]) / 2) + values[1][0] + (values[1][1] - values[1][0])*0.35
	n_min_y = ((values[1][1] - values[1][0]) / 2) + values[1][0] - (values[1][1] - values[1][0])*0.35
	n_max_z = ((values[2][1] + values[2][0]) / 2) + (values[2][1] - values[2][0])*0.35
	n_min_z = ((values[2][1] + values[2][0]) / 2) - (values[2][1] - values[2][0])*0.35
	p = Popen(executable, stdout=PIPE, bufsize=1)
	for line in iter(p.stdout.readline, b''):
		x_right, y_right, z_right = (line.split(",")[i] for i in range(3))
		y_left = line.split(",")[4]
		z_left = line.split(",")[5]
		print line,
		if float(y_right) > n_max_y:	
			with open(file_out, 'w') as f:		
				f.write('up')
				f.flush()
		elif float(y_right) < n_min_y:
			with open(file_out, 'w') as f:
				f.write('down')
				f.flush()
		elif float(x_right) > n_max_x:
			with open(file_out, 'w') as f:		
				f.write('right')
				f.flush()
		elif float(x_right) < n_min_x:
			with open(file_out, 'w') as f:		
				f.write('left')
				f.flush()
		elif float(z_right) > n_max_z:
			with open(file_out, 'w') as f:		
				f.write('back')
				f.flush()
		elif float(z_right) < n_min_z:
			with open(file_out, 'w') as f:		
				f.write('forward')
				f.flush()
		elif float(y_left) >= 0.0 and z_left < n_min_z:
			with open(file_out, 'w') as f:		
				f.write('yaw_right')
				f.flush()
		elif float(y_left) >= 0.0 and z_left > n_max_z:
			with open(file_out, 'w') as f:		
				f.write('yaw_left')
				f.flush()
		elif float(y_right) < n_max_y and float(y_right) > n_min_y and float(x_right) < n_max_x and float(x_right) > n_min_x and float(z_right) < n_max_z and float(z_right) > n_min_z and float(y_left) < 0.0:
			with open(file_out, 'w') as f:		
				f.write('neutral')
				f.flush()
	p.stdout.close()
	p.wait()
def main():
	calibrate_values = calibrate(SKELETAL_EXE_PATH, 30)
	p1 = Process(target = process_motion, args=(SKELETAL_EXE_PATH, OUTPUT_MOTION_FILE_PATH, calibrate_values))
	p1.start()
	p2 = Process(target = process_speech, args=(SPEECH_EXE_PATH, OUTPUT_SPEECH_FILE_PATH))
	p2.start()
if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		print 'Aborting...'
		sys.exit(0)