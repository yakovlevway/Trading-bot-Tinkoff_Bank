import sys
from PyQt5.QtWidgets import QApplication
from App import AppWindow


app = QApplication(sys.argv)
appt = AppWindow()
#appt.run2()
sys.exit(app.exec_())