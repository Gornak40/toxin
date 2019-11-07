import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLineEdit,
    QLCDNumber, QGridLayout, QLabel, QMessageBox,
    QProgressBar, QComboBox, QStatusBar
    )
from PyQt5.QtGui import (
    QIcon, QPixmap
    )
from PyQt5 import QtGui


class ToxinUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.place()
    
    def initUI(self):
        self.resize(300, 200)
        self.setWindowTitle('Toxin')
        self.setWindowIcon(QIcon('icon.ico'))
        self.searchBtn = QPushButton()
        self.searchBtn.setText('Поиск')
        self.lineEdit = QLineEdit()
        self.nameLbl = QLabel()
        #self.nameLbl.setText('Mafia 3') #
        self.downloadBtn = QPushButton()
        self.downloadBtn.setText('Скачать')
        self.nextBtn = QPushButton()
        self.nextBtn.setText('Далее')
        self.picLbl = QLabel()
        #self.picLbl.setPixmap(QPixmap('icon.ico')) #
        self.speedLCD = QLCDNumber()
        self.comboBox = QComboBox()
        #self.comboBox.addItems(['1.torrent', '2.torrent', '3.torrent']) #
        self.progressBar = QProgressBar()
        #self.progressBar.setValue(0) #
        self.cancelBtn = QPushButton()
        self.cancelBtn.setText('Отмена')
        self.donateLbl = QLabel()
        self.donateLbl.setText("""Автор: Александр Горбунов (Gornak40)
Почта: s-kozelsk@yandex.ru
ВК/Телеграм: @gornak40
Github: @Gornak40""")
        self.donateBtn = QPushButton()
        self.donateBtn.setText('Спасибо')
        self.statusBar = QStatusBar()
        self.statusBar.showMessage('Добро пожаловать')
        pal = self.statusBar.palette()
        pal.setColor(QtGui.QPalette.WindowText, QtGui.QColor('green'))
        self.statusBar.setPalette(pal)
        
    def place(self):
        self.grid = QGridLayout()
        self.grid.setSpacing(5)
        self.grid.addWidget(self.lineEdit, 0, 0, 1, 1)
        self.grid.addWidget(self.searchBtn, 0, 1, 1, 1)
        self.grid.addWidget(self.nameLbl, 1, 0, 1, 1)
        self.grid.addWidget(self.nextBtn, 1, 1, 1, 1)
        self.grid.addWidget(self.picLbl, 2, 0, 1, 1)
        self.grid.addWidget(self.speedLCD, 2, 1, 1, 1)
        self.grid.addWidget(self.comboBox, 3, 0, 1, 1)
        self.grid.addWidget(self.downloadBtn, 3, 1, 1, 1)
        self.grid.addWidget(self.progressBar, 4, 0, 1, 1)
        self.grid.addWidget(self.cancelBtn, 4, 1, 1, 1)
        self.grid.addWidget(self.donateLbl, 5, 0, 1, 1)
        self.grid.addWidget(self.donateBtn, 5, 1, 1, 1)
        self.grid.addWidget(self.statusBar, 6, 0, 1, 2)
        self.setLayout(self.grid)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ToxinUI()
    ex.show()
    sys.exit(app.exec())

