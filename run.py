import sys
from PyQt5.QtWidgets import *
from ui_main import Ui_Form

from regular_expression import RegularExpression

class GUI(QDialog):
	def __init__(self):
		super(GUI, self).__init__()

		# Set up the user interface from Designer.
		self.ui = Ui_Form()
		self.ui.setupUi(self)

		# Connect up the buttons.
		self.ui.er_equals_gr_btn.clicked.connect(self.default_button_behavior)
		self.ui.int_fa_a_btn.clicked.connect(self.default_button_behavior)
		self.ui.gr_fa_a_btn.clicked.connect(self.default_button_behavior)
		self.ui.gr_fa_b_btn.clicked.connect(self.default_button_behavior)
		self.ui.min_fa_a_btn.clicked.connect(self.default_button_behavior)
		self.ui.det_af_a_btn.clicked.connect(self.default_button_behavior)
		self.ui.com_fa_a_btn.clicked.connect(self.default_button_behavior)
		self.ui.min_fa_b_btn.clicked.connect(self.default_button_behavior)
		self.ui.det_fa_b_btn.clicked.connect(self.default_button_behavior)
		self.ui.com_fa_b_btn.clicked.connect(self.default_button_behavior)
		self.ui.er_fa_b_btn.clicked.connect(self.default_button_behavior)
		self.ui.er_fa_a_btn.clicked.connect(self.default_button_behavior)
		self.ui.er_search_btn.clicked.connect(self.default_button_behavior)
		self.ui.fa_list_a_btn.clicked.connect(self.default_button_behavior)
		self.ui.fa_list_b_btn.clicked.connect(self.default_button_behavior)

	def default_button_behavior(self):
		print("Not implemented!!!")

app = QApplication(sys.argv)
window = GUI()
window.show()
sys.exit(app.exec_())
