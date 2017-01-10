import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
# implement the default mpl key bindings
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

import tkinter as tk
from tkinter import *
from tkinter.ttk import * 
import random
from time import gmtime, strftime
from PIL import Image, ImageTk
from collections import Counter



class RPSApplication(tk.Frame):
	"""docstring for RPSApplication"""
	def __init__(self, master = None):
		super().__init__(master)
		self.master.title("Rock Paper and Scissors")
		self.master.geometry('700x260+260+260')
		self.master.resizable(width=False, height=False)
		self.pack()

		# game mode
		self.gameMode = "random"

		# statistic
		self.count = 0
		self.winCount = 0
		self.choices = ["Rock", "Paper", "Scissors"]
		self.choicesWin = { "Rock": "Scissors", "Paper": "Rock", "Scissors": "Paper" }
		self.oppoWiseChoices = {"Rock": "Paper", "Paper": "Scissors", "Scissors": "Rock"}
		self.history = []
		self.winningRateHistory = []

		# images
		self.rockImage = ImageTk.PhotoImage(Image.open("rock.png").resize((50, 50), Image.ANTIALIAS))
		self.paperImage = ImageTk.PhotoImage(Image.open("paper.png").resize((50, 50), Image.ANTIALIAS))
		self.scissorImage = ImageTk.PhotoImage(Image.open("scissor.png").resize((50, 50), Image.ANTIALIAS))
		self.imageDic = {"Rock": self.rockImage, "Paper":self.paperImage, "Scissors":self.scissorImage}

		self.create_menu()
		self.create_widgets()

		self.master.lift()
		self.master.attributes('-topmost',True)
		self.master.after_idle(self.master.attributes,'-topmost',False)
		self.master.focus_set()

	def create_menu(self):
		menubar = Menu(self.master)

		# game menu
		GameMenu = Menu(menubar, tearoff=0)
		GameMenu.add_command(label="About", command=lambda: self.showAboutWindow())
		GameMenu.add_command(label="Choose Game Mode", command=self.chooseGameMode)
		GameMenu.add_command(label="Exit", command=self.master.quit)
		menubar.add_cascade(label="Game", menu=GameMenu)

		# game Info
		infomenu = Menu(menubar, tearoff=0)
		infomenu.add_command(label="History", command=lambda: self.showHistory())
		infomenu.add_command(label="Show Winning Rate", command=lambda: self.drawWiningRate())
		menubar.add_cascade(label="Info", menu=infomenu)

		self.master.config(menu=menubar)
		

	def create_widgets(self):
		# create Frames
		self.oppoFrame = tk.Frame(self, borderwidth=1)
		self.resultFrame = tk.Frame(self, borderwidth=1)
		self.myChoicesFrame = tk.Frame(self, borderwidth=1)
		self.analysisFrame = tk.Frame(self, borderwidth=1)

		# pack Frames
		self.analysisFrame.pack(side=BOTTOM,  expand=1)
		self.oppoFrame.pack(side=LEFT,  expand=1)
		self.resultFrame.pack(side=LEFT,  expand=1)
		self.myChoicesFrame.pack(side=RIGHT,  expand=1)
		

		# create oppo and result and analysis
		self.oppoChoice = tk.Label(self.oppoFrame, image = self.imageDic["Rock"])
		self.oppoChoice.image = self.imageDic["Rock"]
		self.result = tk.Label( self.resultFrame, text = "",font = ('Comic Sans MS',20), width=40)
		self.analysis_totalCount = tk.Label( self.analysisFrame, text = "Total Count: 0",font = ('Comic Sans MS',20))
		self.analysis_winningRate = tk.Label( self.analysisFrame, text = "Winning Rate: 0",font = ('Comic Sans MS',20))


		# create RPS labels
		self.Rock = tk.Label(self.myChoicesFrame, image=self.imageDic["Rock"], borderwidth=2)
		self.Paper = tk.Label(self.myChoicesFrame, image=self.imageDic["Paper"], borderwidth=2)
		self.Scissors = tk.Label(self.myChoicesFrame, image=self.imageDic["Scissors"], borderwidth=2)
		self.Rock.image = self.imageDic["Rock"]
		self.Paper.image = self.imageDic["Paper"]
		self.Scissors.image = self.imageDic["Scissors"]
		
		# bind functions to RPS labels
		self.Rock.bind("<Button-1>", lambda _:self.choose("Rock"))
		self.Paper.bind("<Button-1>", lambda _:self.choose("Paper"))
		self.Scissors.bind("<Button-1>", lambda _:self.choose("Scissors"))

		# place all componunt
		self.oppoChoice.pack()
		self.result.pack()
		self.Rock.pack()
		self.Paper.pack()
		self.Scissors.pack()
		self.analysis_totalCount.pack()
		self.analysis_winningRate.pack()

		# set focus and bind key board
		self.myChoicesFrame.focus_set()
		self.myChoicesFrame.bind("j", lambda _:self.choose("Rock")) 
		self.myChoicesFrame.bind("k", lambda _:self.choose("Paper")) 
		self.myChoicesFrame.bind("l", lambda _:self.choose("Scissors")) 

	def choose(self, choice):
		self.setRPGBorder(choice)
		if self.gameMode == "random":
			oppoChoice = random.choice( self.choices )
		else:
			oppoChoice = self.oppoMakeChoice()
		self.oppoChoice.configure(image = self.imageDic[oppoChoice])
		currTime = strftime("%a, %d %b %Y %H:%M:%S", gmtime())
		self.count += 1
		if choice == oppoChoice:
			self.result["text"] = "Tie! Try Again? -_-"					
			singleHistory = ( "tie", choice, currTime )		
		elif self.choicesWin[ choice ] == oppoChoice:
			self.result["text"] = "You win! OMG!!!! O_O"
			singleHistory = ( "win", choice, currTime )
			# self.count += 1
			self.winCount += 1
		else:
			self.result["text"] = "You loser! 2333333"
			singleHistory = ( "lose", choice, currTime )
			# self.count += 1

		self.history.append( singleHistory )
		self.analysis_totalCount["text"] = "Total Count: " + str(self.count)
		winningRate = round(self.winCount/self.count, 2)
		self.analysis_winningRate["text"] = "Wining Rate: " + str(winningRate)
		self.winningRateHistory.append(winningRate)
		# print(singleHistory)

	def oppoMakeChoice(self):
		history = [ x[1] for x in self.history]
		if len(history) < 5:
			return random.choice( self.choices )
		p = random.uniform(0,10)
		# find patterns
		if p <= 7:
			temp = []
			for i in range( len(history)-1 ):
				if history[i] == history[-1]:
					temp.append( history[i+1] )
			if not temp:
				return random.choice( self.choices )
			counter = Counter(temp)
			patterns_choice = counter.most_common(1)[0][0]
			print("pattern choice: ", patterns_choice)
			return self.oppoWiseChoices[patterns_choice]
		# find most common choice
		elif p<= 9:
			p_most_common_choice = self.oppoWiseChoices[ random.choice( history ) ]
			print("most common choice: ", p_most_common_choice)
			return p_most_common_choice
		# random choice
		else:
			random_choice = random.choice( self.choices )
			print("a random choice: ", random_choice)
			return random_choice

	def setRPGBorder(self, choice = None):
		self.Rock['relief'] = 'flat'
		self.Paper['relief'] = 'flat'
		self.Scissors['relief'] = 'flat'
		if choice == "Rock":
			self.Rock['relief'] = 'solid'
		elif choice == "Paper":
			self.Paper['relief'] = 'solid'
		elif choice == "Scissors":
			self.Scissors['relief'] = 'solid'

	def showAboutWindow(self):
		title = "About this game"
		info = "This is just a test game.\n -- Fei"
		version = "0.0.0"
		simpleInfoWindow = tk.Toplevel(self)
		simpleInfoWindow.title(title)
		simpleInfoWindowFrame = tk.Frame(simpleInfoWindow, width=15, height=5)
		infoLable = tk.Label(simpleInfoWindowFrame, text=info, width = 20, height=5)
		infoLable["font"]=('Comic Sans MS',15)
		simpleInfoWindowFrame.pack()
		infoLable.pack()

		versionLable = tk.Label(simpleInfoWindowFrame, text="BTW, the version is: "+version, width = 20, height=5)
		versionLable.pack(side=BOTTOM)

	def chooseGameMode(self):
		gameModeWindow = tk.Toplevel(self)
		gameModeWindow.title("Choose Game Mode")
		frame = tk.Frame(gameModeWindow)
		frame.pack(fill=BOTH, expand=1)

		randomButton = tk.Button(frame, text="Normal", command=self.setRandomMode)
		trainingButton = tk.Button(frame, text="Training", command=self.setTrainingMode)
		randomButton.pack()
		trainingButton.pack()

	def setRandomMode(self):
		self.setRPGBorder()
		self.clearHistory()
		self.gameMode = "random"

	def setTrainingMode(self):
		self.setRPGBorder()
		self.clearHistory()
		self.gameMode = "training"

	def clearHistory(self):
		self.count = 0
		self.winCount = 0
		self.history = []
		self.winningRateHistory = []


	def showHistory(self):
		historyWindow = tk.Toplevel(self)
		historyWindow.title("History")
		frame =  tk.Frame(historyWindow)
		frame.pack()
		scrollbar = Scrollbar(frame)
		scrollbar.pack(side = RIGHT, fill=Y )  

		tv = Treeview(frame)
		tv['columns'] = ('Your Choice' , 'Time')
		tv.heading("#0", text='Result', anchor='w')
		tv.column("#0", anchor="center", width = 50)
		tv.heading('Time', text='Time')
		tv.column('Time', anchor='w', width=200)
		tv.heading('Your Choice', text='Your Choice')
		tv.column('Your Choice', anchor='center', width=100)
		tv.pack(side=LEFT, fill=BOTH)
		
		tv.config(yscrollcommand=scrollbar.set)
		scrollbar.config(command = tv.yview)

		self.historyTreeView = tv
		self.insertHistory()

	def insertHistory(self):
		for singleHistory in self.history:
			self.historyTreeView.insert('', 'end', text=singleHistory[0], values=singleHistory[1:])

	def drawWiningRate(self):
		imageWindow = tk.Toplevel(self)
		imageWindow.title("You winning trend")

		figure = Figure(figsize=(5, 4), dpi=100)
		image = figure.add_subplot(111)
		image.plot(self.winningRateHistory)
		# plt.show()
		canvas = FigureCanvasTkAgg(figure, master=imageWindow)
		canvas.show()
		canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

		canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)

		toolbar = NavigationToolbar2TkAgg(canvas, imageWindow)
		toolbar.update()




root = tk.Tk()
app = RPSApplication(master=root)
app.mainloop()