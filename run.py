import sys
from PyQt5.QtWidgets import *
from main_ui import Ui_Form

from regular_expression import RegularExpression

class MainInit(QDialog):
	def __init__(self):
		super(MainInit, self).__init__()

		# Set up the user interface from Designer.
		self.ui = Ui_Form()
		self.ui.setupUi(self)

		# Connect up the buttons.
		self.ui.regex_to_fa_btn.clicked.connect(self.set_main_automaton_with_regex)

	def fill_table_with_automaton(self, m):
		print(m)

	def set_main_automaton_with_regex(self):
		m = self.get_automatom_from_regex_dialog()
		self.fill_table_with_automaton(m)

	def get_automatom_from_regex_dialog(self):
		s = QInputDialog.getText(self,"Expressão Regular -> FA", "Digite a Expressão Regular a ser convertida")[0]
		r = RegularExpression(s)
		m = r.to_deterministic_finite_automaton()
		return m

app = QApplication(sys.argv)
window = MainInit()
window.show()
sys.exit(app.exec_())
