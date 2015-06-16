import sys
from PyQt5.QtWidgets import QApplication, QDialog
from main_ui import Ui_Form

from regular_expression import RegularExpression

class MainInit(QDialog):
	def __init__(self):
		super(MainInit, self).__init__()

		# Set up the user interface from Designer.
		self.ui = Ui_Form()
		self.ui.setupUi(self)

		# Connect up the buttons.
		self.ui.regex_to_fa_btn.clicked.connect(self.convertTxtToFa)

	def convertTxtToFa(self):
		r = RegularExpression(self.ui.regex_txt.text())
		m = r.to_deterministic_finite_automaton()

		self.ui.fa_table.setSpan(len(m._states),len(m._alphabet)+3)

app = QApplication(sys.argv)
window = MainInit()
window.show()
sys.exit(app.exec_())
