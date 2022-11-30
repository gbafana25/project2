from PyQt5 import uic, QtWidgets
import sys

class Gui(object):
	def load(self):
		super(Gui, self).__init__()
		uic.loadUi("window.ui", self)
		self.show()
