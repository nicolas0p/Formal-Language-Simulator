import sys
from PyQt5.QtWidgets import QApplication, QDialog
from main_ui import Ui_Form

def printHam():
	print("Banana")

class MainInit(QDialog):
	def __init__(self):
		super(MainInit, self).__init__()

		# Set up the user interface from Designer.
		self.ui = Ui_Form()
		self.ui.setupUi(self)

		# Connect up the buttons.
		self.ui.regex_to_fa_btn.clicked.connect(printHam)

app = QApplication(sys.argv)
window = MainInit()
window.show()
sys.exit(app.exec_())
