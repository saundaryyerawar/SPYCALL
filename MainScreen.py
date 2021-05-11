import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFrame, QTabWidget, QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
from Text_File_Analyze_Window import Text_File_Analyze_Window
from Audio_File_Analyze_Window import Audio_File_Analyze_Window


class MainScreen(QWidget):
        
    def __init__(self):
        super().__init__()
        self.resize(700, 500)
        
        self.setWindowTitle("Threat Detection System")
        
        self.layout = QVBoxLayout(self)

        self.title = QLabel()
        self.title.setStyleSheet("font: 75 30pt \"Times New Roman\";\ncolor: rgb(36, 36, 180);\ntext-decoration: underline;")
        self.title.setText("Welcome to Threat Detection System")
        self.layout.addWidget(self.title, 0, Qt.AlignHCenter)

        self.line = QFrame()
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.layout.addWidget(self.line, 0, Qt.AlignBottom)

        self.tabWidget = QTabWidget()

        font = QtGui.QFont()
        font.setPointSize(14)
        self.tabWidget.setFont(font)
        self.tabWidget.setGeometry(QtCore.QRect(14, 9, 721, 371))

        self.Text_File_Analyze_Window = Text_File_Analyze_Window(self)
        self.tabWidget.addTab(self.Text_File_Analyze_Window, "Text File Analyze")

        self.Audio_File_Analyze_Window = Audio_File_Analyze_Window(self)
        self.tabWidget.addTab(self.Audio_File_Analyze_Window, "Audio File Analyze")

        self.layout.addWidget(self.tabWidget)
        self.show()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ex = MainScreen()
    sys.exit(app.exec_())
