import sys
from PyQt5 import QtWidgets 
from game import Game

def main() -> None:
	app = QtWidgets.QApplication(sys.argv)
	win = Game()
	app.exec_()


if __name__ == "__main__":
	main()
