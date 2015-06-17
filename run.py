import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from ui_main import Ui_Form

from regular_expression import RegularExpression

class GUI(QDialog):
	def __init__(self):
		super(GUI, self).__init__()

		# Set up the user interface from Designer.
		self.ui = Ui_Form()
		self.ui.setupUi(self)

		# Connect up the buttons.
		self.ui.er_fa_a_btn.clicked.connect(self.er_fa_a_btn_clicked) # ER -> FA , SLOT A 				## DONE
		self.ui.er_fa_b_btn.clicked.connect(self.er_fa_b_btn_clicked) # ER -> FA, SLOT B 				## DONE
		self.ui.er_search_btn.clicked.connect(self.default_button_behavior) # SEARCH TEXT WITH ER

		self.ui.er_equals_gr_btn.clicked.connect(self.default_button_behavior) # ER EQUIVALENCE GR

		self.ui.gr_fa_a_btn.clicked.connect(self.default_button_behavior) # GR -> FA, SLOT A
		self.ui.gr_fa_b_btn.clicked.connect(self.default_button_behavior) # GR -> FA, SLOT B

		self.ui.det_af_a_btn.clicked.connect(self.det_fa_a_btn_clicked) # DETERMINIZE SLOT A 			## DONE
		self.ui.min_fa_a_btn.clicked.connect(self.min_fa_a_btn_clicked) # MINIMIZE SLOT A 				## DONE
		self.ui.com_fa_a_btn.clicked.connect(self.com_fa_a_btn_clicked) # COMPLEMENT SLOT A 			## DONE

		self.ui.int_fa_a_btn.clicked.connect(self.default_button_behavior) # INTERSECTION SLOT A

		self.ui.det_fa_b_btn.clicked.connect(self.det_fa_b_btn_clicked) # DETERMINE SLOT B 				## DONE
		self.ui.min_fa_b_btn.clicked.connect(self.min_fa_b_btn_clicked) # MINIMIZE SLOT B 				## DONE
		self.ui.com_fa_b_btn.clicked.connect(self.com_fa_b_btn_clicked) # COMPLEMENT SLOT B 			## DONE

		self.ui.fa_list_a_btn.clicked.connect(self.default_button_behavior) # ITEM ON LIST TO SLOT A
		self.ui.fa_list_b_btn.clicked.connect(self.default_button_behavior) # ITEM ON LIST TO SLOT B

	def default_button_behavior(self):
		print("Not implemented!!!")

	def er_fa_a_btn_clicked(self):
		self.er_fa_btn_clicked('a')

	def er_fa_b_btn_clicked(self):
		self.er_fa_btn_clicked('b')

	def er_fa_btn_clicked(self,table):
		st = self.ui.er_text.toPlainText()

		if st == '':
			st = "(0*(1(01*0)*1)*0*)*"

		fa = RegularExpression(st).to_deterministic_finite_automaton()

		# TODO: store fa on sidelist

		self.set_fa_on_table(fa,table)

	def det_fa_a_btn_clicked(self):
		# TODO: show error if nothing on _fa_a
		self._fa_a.determinize()
		self.set_fa_on_table(self._fa_a, 'a')

	def det_fa_b_btn_clicked(self):
		# TODO: show error if nothing on _fa_b
		self._fa_b.determinize()
		self.set_fa_on_table(self._fa_b, 'b')

	def min_fa_a_btn_clicked(self):
		# TODO: show error if nothing on _fa_a
		self._fa_a.minimize()
		self.set_fa_on_table(self._fa_a, 'a')

	def min_fa_b_btn_clicked(self):
		# TODO: show error if nothing on _fa_b
		self._fa_b.minimize()
		self.set_fa_on_table(self._fa_b, 'b')

	def com_fa_a_btn_clicked(self):
		# TODO: show error if nothing on _fa_a
		a = self._fa_a.complement()
		self.set_fa_on_table(a, 'a')

	def com_fa_b_btn_clicked(self):
		# TODO: show error if nothing on _fa_b
		b = self._fa_b.complement()
		self.set_fa_on_table(b, 'b')

	def set_fa_on_table(self, fa, table):
		if table == 'a':
			table = self.ui.fa_a_table
			self._fa_a = fa
		elif table == 'b':
			table = self.ui.fa_b_table
			self._fa_b = fa

		# table.setRowCount(7);
		# table.setColumnCount(3);
		#
		# table.setHorizontalHeaderLabels(['Banana','Laranja','Tomate'])
		#
		# table.setItem(0, 0, QTableWidgetItem("Exemplo"))

		states = list(fa._states)
		alphabet = list(fa._alphabet)

		table.setRowCount(len(states))
		table.setColumnCount(len(alphabet))

		table.setHorizontalHeaderLabels(alphabet)

		state_labels = ["" for state in states]
		for i in range(len(states)):
			if states[i] == fa._initial_state:
				state_labels[i] += "->"
			if states[i] in fa._final_states:
				state_labels[i] += "*"
			state_labels[i] += states[i]._name
		table.setVerticalHeaderLabels(state_labels)

		for i in range(len(states)):
			state = states[i]
			for j in range(len(alphabet)):
				symbol = alphabet[j]
				transitions = list(fa._transitions[state][symbol])
				s = "-"
				if len(transitions) == 1:
					s = transitions[0].__repr__()
				elif len(transitions) > 1:
					s = transitions.__str__()

				table.setItem(i,j,QTableWidgetItem(s))

		table.resizeColumnsToContents()
		table.resizeRowsToContents()



app = QApplication(sys.argv)
window = GUI()
window.show()
sys.exit(app.exec_())
