from gui import Gui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import * 
from PyQt5.QtGui import *
import sys
import random

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

class Game(QMainWindow, Gui):

	"""
	Class that handles the input and main logic of the game

	Class Variables:
	:param current_row: index of current guess
	:param guess_array: matrix of each row of text input
	:param wrong_letters: displays incorrect letters
	:param flags: indicates if character has already been guessed
	:param green: green color QPalette object
	:param yellow: yellow color QPalette object
	:param gray: gray color QPalette object
	:param rand_word: randomly-selected word
	"""

	def get_random_word() -> str:
		"""
		picks a random word from wordlist

		Wordlist source: https://gist.github.com/cfreshman/a7b776506c73284511034e63af1017ee 

		:return: Random string
		"""
		f = open("wordlist", "r")
		words = f.read().splitlines()
		return words[random.randint(0, 2309)]

	current_row = 0
	guess_array = []
	wrong_letters = []
	flags = [False, False, False, False, False]
	green = QPalette()
	yellow = QPalette()
	gray = QPalette()
	green.setColor(green.Base, QColor(38, 230, 0))
	yellow.setColor(yellow.Base, QColor(255, 230, 102))
	gray.setColor(gray.Base, QColor(232, 232, 232))
	rand_word = get_random_word()

	def create_guess_array(self) -> [QLineEdit]:
		array = []
		grid = self.guesses
		for i in range(grid.count()):
			row = []
			for j in range(grid.itemAt(i).count()):
				row.append(grid.itemAt(i).itemAt(j).widget())
			array.append(row)
				
		return array
	
	def disable_row(self, row) -> None:
		"""
		disables a row
		:param row: Array of QLineEdit
		"""
		for line in row:
			line.setEnabled(False)	

	def enable_row(self, row) -> None:
		"""
		enables a row
		:param row: Array of QLineEdit
		"""
		for line in row:
			line.setEnabled(True)

	def read_only_row(self, row) -> None:
		"""
		makes a row read only (not grayed out)
		:param row: Array of QLineEdit
		"""
		for line in row:
			line.setReadOnly(True)

	def start_game(self, grid) -> None:
		"""
		disables all rows except the first when game starts
		:param grid: matrix of List[QLineEdit]
		"""
		for i in range(1, len(grid)):
			self.disable_row(grid[i])
	
	def is_in_word(self, ch, pos, guess) -> bool:
		"""
		checks if a letter is in a word, but not in the right spot
		and hasn't been guessed yet.

		:param ch: character that was given
		:param pos: position of ch
		:param guess: entire guess

		:return: True or False
		"""
		for i in range(len(self.rand_word)):
			if ch == self.rand_word[i] and pos != i:
				if self.flags[i] == False and ch not in guess[pos+1:]: 
					return True
				
				
		return False

	def check_empty(self, row) -> bool:
		"""
		checks if a row is empty

		:param row: Array of QLineEdit

		:return: True or False
		"""
		word = ""
		for i in row:
			word += i.text()	
		if len(word) == 5:
			return True
		return False


	def display_wrong(self, ch) -> None:
		"""
		displays an incorrect character in a label 

		:param ch: incorrect character
		"""
		wr = ""
		if ch not in self.wrong_letters:
			self.wrong_letters.append(ch)
		for w in self.wrong_letters:
			wr += w
			wr += " "
		self.wrong_label.setText(wr)

	def check_row(self) -> None:
		"""
		gets triggered whenever Enter button is pressed	
		"""
		was_empty = False
		# holds all guessed characters in one string
		guessed = ""
		# has to be reset every guess
		self.flags = [False, False, False, False, False]
		r = self.guess_array[self.current_row]
		if self.check_empty(r) == False:
			self.id.setText("ERROR - blank input")
			return None

		for i in range(len(r)):
			guessed += r[i].text()

		for i in range(len(guessed)):	
			if guessed[i] == self.rand_word[i]:
				self.flags[i] = True
				r[i].setPalette(self.green)
			elif self.is_in_word(guessed[i], i, guessed) == True:
				r[i].setPalette(self.yellow)
				self.flags[i] = False	
			else:
				self.display_wrong(guessed[i])
				r[i].setPalette(self.gray)
				self.flags[i] = False

		# if all flags are set to true, then the game is over
		if False not in self.flags:
			self.id.setText("")
			self.wrong_label.setText("You won")
			self.read_only_row(self.guess_array[self.current_row])
		# no more rows left, game is over
		elif self.current_row == 5:
			self.id.setText("Answer:")
			self.wrong_label.setText(self.rand_word)
			self.disable_row(self.guess_array[5])
		# continue the game
		else:
			self.current_row += 1
			for element in r:
				element.setEnabled(False)
			self.enable_row(self.guess_array[self.current_row])
		
		


	def __init__(self) -> None:
		super().__init__()
		self.load()
		self.guess_array = self.create_guess_array()
		self.submit.clicked.connect(self.check_row)
		self.start_game(self.guess_array)
