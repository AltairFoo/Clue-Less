# client.py

# EN.605.601.81.SP22 (Foundations of Software Engineering)
# Authors: Tenth Floor Cool Kids Club

import sys
import threading
import socket

from PyQt6.QtCore import QThread, pyqtSignal, QObject

class Client(QThread):
    s_connect = pyqtSignal(bool)
    s_playerName = pyqtSignal()

    def __init__(self, parent, serverAddress: str):
        super().__init__()
        self.host = serverAddress
        self.gui = parent
        self.connectSocket()
        self.s_connect.connect(self.gui.s_connect.emit)
        self.s_playerName.connect(self.gui.s_playerName.emit)

    def connectSocket(self):
        try:
            print('Attempting Connection..')
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect((self.host, 8080))
            print('Connection Successful!')
        except Exception as connection_failed:
            print(f'Error: Unable to connect to host {self.host}. Is the server currently running?')
            self.s_connect.emit(False)
        rx_thread = threading.Thread(target=self.rx_server, daemon = True) # Receive communication on a separate thread
        rx_thread.start()
        #self.tx_server("") # Transmit communication from the main thread
        self.s_connect.emit(True)

    def tx_server(self, input: str):
        '''Transmit communication to server'''
        try:
            self.client.send(input.encode('utf-8'))
        except Exception as tx_error:
            print(f'Error: Unable to message server: {tx_error}')
            

    def rx_server(self):
        '''Receive communication from server.'''
        while 1:
            try:
                msg = self.client.recv(3000).decode('utf-8')
                if msg:
                    if(msg == 'kick'):
                        #print('You have been disconnected from the server.')
                        self.client.shutdown(socket.SHUT_RDWR)
                        self.client.close()
                        #establiosh connection again, this is causing error
                        #self.connectSocket()
                    else:
                        print("Get Command From Server:")
                        if msg == "What would you like your username to be?: ":
                            self.s_playerName.emit()
                        print(msg)
                else:
                    break
            except Exception as rx_error:
                print('You have been disconnected from the server.')
                self.s_connect.emit(False)
                break
