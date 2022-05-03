# UI_Client.py

# EN.605.601.81.SP22 (Foundations of Software Engineering)
# Authors: Tenth Floor Cool Kids Club

from PyQt6.QtWidgets import *
from PyQt6 import uic
from PyQt6.QtCore import QThread, pyqtSignal, QObject
from UI_Client import MainWindow

class GamePlayWindow():
    def __init__(self):
        uic.loadUi(".\\views\\ClueStart.ui", self)
        
    def newPage(self, MainWindow):
        self.centralwidget = QWidget(MainWindow)