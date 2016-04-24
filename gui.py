import os
from Tkinter import *
from ttk import Frame, Button, Style

class Example(Frame):
	def __init__(self, parent):
		Frame.__init__(self, parent)   
		self.parent = parent
		self.initUI()
	def initUI(self):
		self.parent.title("Kinect Controlled Quadcopter")
		self.style = Style()
		self.style.theme_use("default")
		frame = Frame(self, relief=RAISED, borderwidth=1)
		frame.pack(fill=BOTH, expand=True)
		self.pack(fill=BOTH, expand=True)
		run_button = Button(self, text="Run", command = self.openFile)
		run_button.pack(side=RIGHT)
	def openFile(self):
		os.startfile('data_processing.pyc')
def main():
	root = Tk()
	root.geometry("300x200+300+300")
	app = Example(root)
	root.mainloop()  
if __name__ == '__main__':
	main() 