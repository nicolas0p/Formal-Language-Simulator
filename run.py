import sys
from PyQt5.QtWidgets import QApplication, QDialog
from main_ui import Ui_Form  # here you need to correct the names

app = QApplication(sys.argv)
window = QDialog()
ui = Ui_Form()
ui.setupUi(window)

window.show()
sys.exit(app.exec_())
