from PyQt5.QtWidgets import QApplication
import sys
from gui import MainWidget


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWidget()
    sys.exit(app.exec_())