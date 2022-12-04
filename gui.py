from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import * 
from PyQt5.QtGui import *
import sys

class Gui(object):
	"""
	Loads all graphical elements from .ui file
	"""
	def load(self) -> None:	
		super(Gui, self).__init__()
		uic.loadUi("window.ui", self)
		self.show()
