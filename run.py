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
		self.ui.er_fa_a_btn.clicked.connect(self.er_fa_a_btn_clicked) # ER -> FA , SLOT A
		self.ui.er_fa_b_btn.clicked.connect(self.default_button_behavior) # ER -> FA, SLOT B
		self.ui.er_search_btn.clicked.connect(self.default_button_behavior) # SEARCH TEXT WITH ER

		self.ui.er_equals_gr_btn.clicked.connect(self.default_button_behavior) # ER EQUIVALENCE GR

		self.ui.gr_fa_a_btn.clicked.connect(self.default_button_behavior) # GR -> FA, SLOT A
		self.ui.gr_fa_b_btn.clicked.connect(self.default_button_behavior) # GR -> FA, SLOT B

		self.ui.det_af_a_btn.clicked.connect(self.default_button_behavior) # DETERMINIZE SLOT A
		self.ui.min_fa_a_btn.clicked.connect(self.default_button_behavior) # MINIMIZE SLOT A
		self.ui.com_fa_a_btn.clicked.connect(self.default_button_behavior) # COMPLEMENT SLOT A

		self.ui.int_fa_a_btn.clicked.connect(self.default_button_behavior) # INTERSECTION SLOT A

		self.ui.det_fa_b_btn.clicked.connect(self.default_button_behavior) # DETERMINE SLOT B
		self.ui.min_fa_b_btn.clicked.connect(self.default_button_behavior) # MINIMIZE SLOT B
		self.ui.com_fa_b_btn.clicked.connect(self.default_button_behavior) # COMPLEMENT SLOT B

		self.ui.fa_list_a_btn.clicked.connect(self.default_button_behavior) # ITEM ON LIST TO SLOT A
		self.ui.fa_list_b_btn.clicked.connect(self.default_button_behavior) # ITEM ON LIST TO SLOT B

	def default_button_behavior(self):
		print("Not implemented!!!")

	def er_fa_a_btn_clicked(self):
		self.set_fa_on_table(0,'a')

	def set_fa_on_table(self, fa, table):
		if table == 'a':
			table = self.ui.fa_a_table
		elif table == 'b':
			table = self.ui.fa_b_table

		table.setRowCount(7);
		table.setColumnCount(3);

		table.setHorizontalHeaderLabels(['Banana','Laranja','Tomate'])

		table.setItem(0, 0, QTableWidgetItem("Exemplo"))

app = QApplication(sys.argv)
window = GUI()
window.show()
sys.exit(app.exec_())
