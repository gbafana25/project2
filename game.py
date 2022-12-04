from gui import Gui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import * 
from PyQt5.QtGui import *
import sys
import random

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class Game(QMainWindow, Gui):

	def get_random_word():
		f = open("wordlist", "r")
		words = f.read().splitlines()
		return words[random.randint(0, 2309)]

	current_row = 0
	guess_array = []
	wrong = []
	flags = [False, False, False, False, False]
	green = QPalette()
	yellow = QPalette()
	gray = QPalette()
	green.setColor(green.Base, QColor(38, 230, 0))
	yellow.setColor(yellow.Base, QColor(255, 230, 102))
	gray.setColor(gray.Base, QColor(232, 232, 232))
	rand_word = get_random_word()

	def create_guess_array(self):
		array = []
		grid = self.guesses
		for i in range(grid.count()):
			row = []
			for j in range(grid.itemAt(i).count()):
				row.append(grid.itemAt(i).itemAt(j).widget())
			array.append(row)
				
		return array
	
	def disable_row(self, row):
		for line in row:
			line.setEnabled(False)	

	def enable_row(self, row):
		for line in row:
			line.setEnabled(True)

	def read_only_row(self, row):
		for line in row:
			line.setReadOnly(True)

	def start_game(self, g):
		for i in range(1, len(g)):
			self.disable_row(g[i])


	
	def is_in_word(self, c, pos, word, guess):
		for i in range(len(word)):
			if c == word[i] and pos != i:
				if self.flags[i] == False and c not in guess[pos+1:]: 
					return True
				
				
		return False

	def check_empty(self, row):
		word = ""
		for i in row:
			word += i.text()	
		if len(word) == 5:
			return True
		return False


	def display_wrong(self, l):
		wr = ""
		if l not in self.wrong:
			self.wrong.append(l)
		for w in self.wrong:
			wr += w
			wr += " "
		self.wrong_letters.setText(wr)

	def check_row(self):
		was_empty = False
		guessed = ""
		self.flags = [False, False, False, False, False]
		r = self.guess_array[self.current_row]
		if self.check_empty(r) == False:
			self.id.setText("ERROR - blank input")
			return 0

		for i in range(len(r)):
			guessed += r[i].text()

		for i in range(len(guessed)):
			if guessed[i] == '':
				was_empty = True
				break
			elif guessed[i] == self.rand_word[i]:
				self.flags[i] = True
				r[i].setPalette(self.green)
			elif self.is_in_word(guessed[i], i, self.rand_word, guessed) == True:
				r[i].setPalette(self.yellow)
				self.flags[i] = False	
			else:
				self.display_wrong(guessed[i])
				r[i].setPalette(self.gray)
				self.flags[i] = False

		# if all flags are set to true, then the game is over
		if False not in self.flags:
			self.id.setText("")
			self.wrong_letters.setText("You won")
			self.read_only_row(self.guess_array[self.current_row])
		elif self.current_row == 5:
			self.id.setText("Answer:")
			self.wrong_letters.setText(self.rand_word)
			self.disable_row(self.guess_array[5])
		else:
			if was_empty == False:
				self.current_row += 1
				for element in r:
					element.setEnabled(False)
				self.enable_row(self.guess_array[self.current_row])
		
		


	def __init__(self):
		super().__init__()
		self.load()
		self.guess_array = self.create_guess_array()
		self.submit.clicked.connect(self.check_row)
		self.start_game(self.guess_array)
