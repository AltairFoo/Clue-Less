# UI_Client.py

# EN.605.601.81.SP22 (Foundations of Software Engineering)
# Authors: Tenth Floor Cool Kids Club
# darkmode color design guide: https://uxdesign.cc/dark-mode-ui-design-the-definitive-guide-part-1-color-53dcfaea5129
# style sheet: https://doc.qt.io/qt-5/stylesheet-reference.html

import sys
import threading

from PyQt6.QtWidgets import *
from PyQt6 import uic
from PyQt6.QtCore import QThread, pyqtSignal

from client import Client

#region global variables
_IsGameSessionJoined = False
_ServerAddress = ""
_PlayerName = ""
#endregion global variables

class MainWindow(QMainWindow):

    #region binding pyqtSignal
    s_connect = pyqtSignal(bool)
    s_playerName = pyqtSignal()
    s_startGame = pyqtSignal()
    s_assignCharacter = pyqtSignal(list)
    #endregion binding pyqtSignal

    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi(".\\views\\ClueStart_Main.ui", self)
        self.intializeComponents()
        self.signalBinding()
        self.show()

    def intializeComponents(self):
        self.ui.Btn_JoinServer.clicked.connect(self.joinServer)
        #self.ui.Btn_JoinServer.clicked.connect(self.startGame)
        self.ui.Widget_ConfirmPlayer.setVisible(False)
        self.ui.Btn_ConfirmPlayer.clicked.connect(self.sendPlayerName)
        self.ui.Widget_GamePlay.setVisible(False)

    def signalBinding(self):
        self.s_connect.connect(self.updateJoinServerGUI)
        self.s_playerName.connect(self.enterPlayerName)
        self.s_startGame.connect(self.startGame)
        self.s_assignCharacter.connect(self.pickCharacter)

    def closeEvent(self, e):
        global _IsGameSessionJoined
        if _IsGameSessionJoined:
            answer = QMessageBox.question(
                window, None,
                "A game session is connected. Close the game?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            # the anwser correspond to the button type
            if answer == QMessageBox.StandardButton.Yes:
                app.quit()
            else:
                e.ignore()
        else:
            # straight forward game quit or have a question box.
            app.quit()

    def joinServer(self):
        serverAddress = self.ui.Entry.text()
        if len(serverAddress) == 0 or not serverAddress or serverAddress.isspace():
            print("No server address")
        else:
            # strip before connecting
            serverAddress = serverAddress.strip()
            global _ServerAddress
            _ServerAddress = serverAddress
            self.createGameClient()
            
    def createGameClient(self):
        global _ServerAddress
        self.gameClient = Client(self, _ServerAddress)
        self.gameClient.start()

    def updateJoinServerGUI(self, isConnected: bool):
        if isConnected:
            self.ui.Btn_JoinServer.setText("Enjoy!")
            self.ui.Btn_JoinServer.setEnabled(False)
            # remove any error messages
            self.ui.Label_JoinErrorMsg.setText("")
            global _IsGameSessionJoined
            _IsGameSessionJoined = True
        else:
            global _ServerAddress
            self.ui.Label_JoinErrorMsg.setText(f"Unable to connect to host {_ServerAddress}. Is the server currently running?")
            self.ui.Btn_JoinServer.setText("Join Server")
            self.ui.Btn_JoinServer.setEnabled(True)
            _ServerAddress = ""
        pass

    def enterPlayerName(self):
        print("enterPlayerName")
        self.ui.Widget_JoinServer.setVisible(False)
        self.ui.Widget_ConfirmPlayer.setVisible(True)
        # change button to enter game
        self.ui.Btn_JoinServer.setText("Enter")
        self.ui.Btn_JoinServer.setEnabled(True)
        # spawn enter nane ui
        self.ui.EntryLabel.setText("PlayerName")
        self.ui.Entry.setText("")
        pass
    
    def sendPlayerName(self):
        global _PlayerName
        _PlayerName = self.ui.Entry_2.text()
        self.gameClient.tx_server(_PlayerName)

    def startGame(self):
        self.ui.Widget_GameInit.setVisible(False)
        self.ui.Widget_GamePlay.setVisible(True)
        self.show()
        print("StartGame")

    def pickCharacter(self, characterOptions: list):
        print("options: ", characterOptions)
        self.show()
        

app = QApplication(sys.argv)
window = MainWindow()
app.exec()
