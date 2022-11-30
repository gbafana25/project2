from gui import Gui
from PyQt5 import QtWidgets, QtCore
import sys

class Game(QtWidgets.QMainWindow, Gui):
	def __init__(self):
		super().__init__()
		self.load()

