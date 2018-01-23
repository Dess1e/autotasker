from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout, QLineEdit, QFileDialog, QLabel, QCheckBox
from PyQt5.QtCore import QDir


class DialogWidget(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.doneButton = QPushButton(self)
        self.cancelButton = QPushButton(self)
        self.setGeometry(300, 300, 300, 300)
        f = lambda: self.parent.pushDialogKwargs(self.makeKwargs())
        f_c = lambda: self.parent.pushDialogKwargs(None)
        self.doneButton.clicked.connect(f)
        self.cancelButton.clicked.connect(f_c)
        self.init()

    def init(self):
        self.doneButton.setText('Done')
        self.cancelButton.setText('Cancel')

    def makeKwargs(self):
        pass


class DialogTimer(DialogWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setLayout(QGridLayout())
        self.timeLine = QLineEdit(self)
        self.setWindowTitle('Select timer properties')
        self.layout().addWidget(self.timeLine, 0, 0, 1, 2)
        self.layout().addWidget(self.doneButton, 1, 0)
        self.layout().addWidget(self.cancelButton, 1, 1)
        self.show()

    def makeKwargs(self):
        kwargs = {'time': self.timeLine.text()}
        return kwargs


class DialogAlerter(DialogWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setLayout(QGridLayout())
        self.textLine = QLineEdit(self)
        self.setWindowTitle('Select alert message properties')
        self.layout().addWidget(self.textLine, 0, 0, 1, 2)
        self.layout().addWidget(self.doneButton, 1, 0)
        self.layout().addWidget(self.cancelButton, 1, 1)
        self.show()

    def makeKwargs(self):
        kwargs = {'text': self.textLine.text()}
        return kwargs


class DialogClicker(DialogWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setLayout(QGridLayout())
        self.xline = QLineEdit(self)
        self.yline = QLineEdit(self)
        self.setWindowTitle('Select clicker properies')
        self.layout().addWidget(self.xline, 0, 0)
        self.layout().addWidget(self.yline, 0, 1)
        self.layout().addWidget(self.doneButton, 1, 0)
        self.layout().addWidget(self.cancelButton, 1, 1)
        self.show()

    def makeKwargs(self):
        kwargs = {'x': self.xline.text(), 'y': self.yline.text()}
        return kwargs


class DialogFindAndClick(DialogWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setLayout(QGridLayout())
        self.setWindowTitle('Select image to find and click...')
        self.browse = QPushButton('Browse')
        self.label = QLabel('Click browse to select image')
        self.labelpath = QLabel('')
        self.checkbox = QCheckBox('Continue if can\'t match')
        self.layout().addWidget(self.label, 0, 0)
        self.layout().addWidget(self.labelpath, 1, 0)
        self.layout().addWidget(self.browse, 2, 0, 1, 2)
        self.layout().addWidget(self.checkbox, 3, 0)
        self.layout().addWidget(self.doneButton, 4, 0)
        self.layout().addWidget(self.cancelButton, 4, 1)
        self.browse.clicked.connect(self.browseClicked)
        self.show()

    def browseClicked(self):
        st = QFileDialog.getOpenFileName(parent=self,
                                         caption='Select image to find',
                                         directory=QDir.currentPath())
        if st[0]:
            self.labelpath.setText(st[0])

    def makeKwargs(self):
        path = self.labelpath.text()
        if path:
            kwargs = {'path': path,
                      'continueIfNotFound': self.checkbox.isChecked()}
            return kwargs
        else:
            return None


