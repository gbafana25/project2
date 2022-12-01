from gui import Gui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import * 
from PyQt5.QtGui import *
import sys

class Game(QMainWindow, Gui):
	current_row = 0
	guess_array = []
	flags = [False, False, False, False, False]

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
		for line in guess_array[row]:
			line.setEnabled(False)	

	def is_in_word(self, c, pos, word):
		if c in word:
			for i in range(len(word)):
				if c == word[i] and pos != i and self.flags[i] == False:
					return True
				"""
				elif c == word[i] and flags[i] == True:
					return False
				"""
		return False					

	def check_row(self):
		# placeholder word
		word = "crane"
		r = self.guess_array[self.current_row]
		for i in range(len(r)):
			letter = r[i].text()	
			if letter == word[i]:
				print(f'Letter {letter} correct')
				self.flags[i] = True
			elif self.is_in_word(letter, i, word) == True:
				print(f'{letter} is somewhere else')
			elif letter == '':
				print('Error - blank input')
				break
			else:
				print(f'{letter} not in word')
		print(self.flags)
		
		self.current_row += 1
		print()
		


	def __init__(self):
		super().__init__()
		self.load()
		self.guess_array = self.create_guess_array()
		self.submit.clicked.connect(self.check_row)
		#self.disable_row(guesses, 1)
