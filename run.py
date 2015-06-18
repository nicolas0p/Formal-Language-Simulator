import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from ui_main import Ui_Form

from regular_expression import RegularExpression
from grammar import Grammar

class GUI(QDialog):
	def __init__(self):
		super(GUI, self).__init__()

		# Set up the user interface from Designer.
		self.ui = Ui_Form()
		self.ui.setupUi(self)

		# Connect up the buttons.
		self.ui.er_fa_a_btn.clicked.connect(self.er_fa_a_btn_clicked) # ER -> FA , SLOT A 				## DONE
		self.ui.er_fa_b_btn.clicked.connect(self.er_fa_b_btn_clicked) # ER -> FA, SLOT B 				## DONE

		self.ui.er_search_btn.clicked.connect(self.default_button_behavior) # SEARCH TEXT WITH ER		#

		self.ui.er_equals_gr_btn.clicked.connect(self.er_equals_gr_btn_clicked) # ER EQUIVALENCE GR		#

		self.ui.gr_fa_a_btn.clicked.connect(self.gr_fa_a_btn_clicked) # GR -> FA, SLOT A				## DONE
		self.ui.gr_fa_b_btn.clicked.connect(self.gr_fa_b_btn_clicked) # GR -> FA, SLOT B				## DONE

		self.ui.det_fa_a_btn.clicked.connect(self.det_fa_a_btn_clicked) # DETERMINIZE SLOT A 			## DONE
		self.ui.min_fa_a_btn.clicked.connect(self.min_fa_a_btn_clicked) # MINIMIZE SLOT A 				## DONE
		self.ui.com_fa_a_btn.clicked.connect(self.com_fa_a_btn_clicked) # COMPLEMENT SLOT A 			## DONE

		self.ui.int_fa_a_btn.clicked.connect(self.int_fa_a_btn_clicked) # INTERSECTION SLOT A           ## DONE

		self.ui.det_fa_b_btn.clicked.connect(self.det_fa_b_btn_clicked) # DETERMINE SLOT B 				## DONE
		self.ui.min_fa_b_btn.clicked.connect(self.min_fa_b_btn_clicked) # MINIMIZE SLOT B 				## DONE
		self.ui.com_fa_b_btn.clicked.connect(self.com_fa_b_btn_clicked) # COMPLEMENT SLOT B 			## DONE

		self.ui.fa_list_a_btn.clicked.connect(self.fa_list_a_btn_clicked) # ITEM ON LIST TO SLOT A		## DONE
		self.ui.fa_list_b_btn.clicked.connect(self.fa_list_b_btn_clicked) # ITEM ON LIST TO SLOT B		## DONE

		self._fa_a = None
		self._fa_b = None
		self._fa_list = {}

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
		self.add_fa_on_list('ER => FA', fa)
		self.set_fa_on_table(fa,table)

	def gr_fa_a_btn_clicked(self):
		self.gr_fa_btn_clicked('a')

	def gr_fa_b_btn_clicked(self):
		self.gr_fa_btn_clicked('b')

	def gr_fa_btn_clicked(self, table):
		st = self.ui.gr_text.toPlainText()
		if st == '':
			st = "S -> aS | a | bS | b"

		gr = Grammar.text_to_grammar(st)
		fa = gr.to_finite_automaton()

		self.add_fa_on_list("GR => FA", fa)
		self.set_fa_on_table(fa, table)

	def er_equals_gr_btn_clicked(self):
		st = self.ui.gr_text.toPlainText()
		if st == '':
			st = "S -> aS | a | bS | b"
		gr = Grammar.text_to_grammar(st)
		fa_gr = gr.to_finite_automaton()

		st = self.ui.er_text.toPlainText()
		if st == '':
			st = "(0*(1(01*0)*1)*0*)*"
		fa_er = RegularExpression(st).to_deterministic_finite_automaton()

		if fa_gr.is_equal(fa_er):
			QMessageBox.about(self,"Equivalência entre GR e ER","A Expressão Regular é equivalente à Gramática Regular")
		else:
			QMessageBox.about(self,"Equivalência entre GR e ER","A Expressão Regular NÃO é equivalente à Gramática Regular")


	def det_fa_a_btn_clicked(self):
		self.det_fa_btn_clicked(self._fa_a, 'a')

	def det_fa_b_btn_clicked(self):
		self.det_fa_btn_clicked(self._fa_b, 'b')

	def det_fa_btn_clicked(self, fa, table):
		if fa == None:
			print("Não há autômato no Slot")
			return

		fa = fa.copy()

		fa.determinize()
		self.add_fa_on_list('Determinização - Slot %s'%(table.capitalize()), fa)
		self.set_fa_on_table(fa, table)

	def min_fa_a_btn_clicked(self):
		self.min_fa_btn_clicked(self._fa_a, 'a')

	def min_fa_b_btn_clicked(self):
		self.min_fa_btn_clicked(self._fa_b, 'b')

	def min_fa_btn_clicked(self, fa, table):
		if fa == None:
			print("Não há autômato no Slot")
			return

		fa = fa.copy()

		fa.minimize()
		self.add_fa_on_list('Minimização - Slot %s'%(table.capitalize()), fa)
		self.set_fa_on_table(fa, table)

	def com_fa_a_btn_clicked(self):
		self.com_fa_btn_clicked(self._fa_a, 'a')

	def com_fa_b_btn_clicked(self):
		self.com_fa_btn_clicked(self._fa_b, 'b')

	def com_fa_btn_clicked(self, fa, table):
		if fa == None:
			print("Não há autômato no Slot")
			return

		fa = fa.complement()
		self.add_fa_on_list('Complemento - Slot %s'%(table.capitalize()), fa)
		self.set_fa_on_table(fa, table)

	def int_fa_a_btn_clicked(self):
		if self._fa_a == None or self._fa_b == None:
			print("Não há autômato em algum slot")
			return

		fa = self._fa_a.intersection(self._fa_b)
		self.add_fa_on_list('Intersecção entre AFs', fa)
		self.set_fa_on_table(fa, 'a')

	def fa_list_a_btn_clicked(self):
		fa = self.get_selected_fa_from_list()
		self.set_fa_on_table(fa, 'a')

	def fa_list_b_btn_clicked(self):
		fa = self.get_selected_fa_from_list()
		self.set_fa_on_table(fa, 'b')

	def add_fa_on_list(self, name, fa):
		# self.ui.listWidget.addItem("123 banana!")
		name = "#%d %s"%(self.ui.listWidget.count(),name)
		self.ui.listWidget.addItem(name);
		self._fa_list[name] = fa

	def get_selected_fa_from_list(self):
		return self._fa_list[self.ui.listWidget.currentItem().text()]

	def set_fa_on_table(self, fa, table):
		if table == 'a':
			table = self.ui.fa_a_table
			self._fa_a = fa
		elif table == 'b':
			table = self.ui.fa_b_table
			self._fa_b = fa

		fa = fa.copy()
		fa.rename_states()

		# table.setRowCount(7);
		# table.setColumnCount(3);
		#
		# table.setHorizontalHeaderLabels(['Banana','Laranja','Tomate'])
		#
		# table.setItem(0, 0, QTableWidgetItem("Exemplo"))

		states = list(fa._states)
		alphabet = list(fa._alphabet)

		if not fa.is_nondeterministic():
			alphabet.remove('&')

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
