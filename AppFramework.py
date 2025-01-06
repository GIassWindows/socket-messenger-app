import sys
import socket
import threading
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QLineEdit, QHBoxLayout, QScrollArea
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class SocketMessage:
    is_Server = False
    is_Client = False
    can_use = False
    server_ip = "" # your public ip here
    port = "25555"
    server = None
    client = None

    def __init__(self):
        # all things window size
        self.app = QApplication(sys.argv)
        self.window = QWidget()
        self.window.setWindowTitle("IPC Socket Messenger")
        self.window.setGeometry(500,500,750,500)

        # contents of app
        self.layout = QVBoxLayout()
        self.buttonLayout = QHBoxLayout()
        self.serverButton = QPushButton("Create Server")
        self.clientButton = QPushButton("Join Server as Client")
        self.label = QLabel()
        self.scroller = QScrollArea()
        self.textbox = QLineEdit()

        # edits
        self.scroller.setWidgetResizable(True)
        self.font = QFont("Rubik", 20)
        self.label.setFont(self.font)

        # initialise
        self.scroller.setWidget(self.label)
        self.layout.addWidget(self.textbox)
        self.buttonLayout.addWidget(self.serverButton)
        self.buttonLayout.addWidget(self.clientButton)
        self.layout.addWidget(self.scroller)
        self.layout.addLayout(self.buttonLayout)
        self.window.setLayout(self.layout)

    def createServer(self):
        if self.is_Client or self.is_Server:
            return
        
        self.is_Server = True
        self.window.setWindowTitle("Server @Port: " + self.port)

        self.label.setText(self.label.text() + f"\n Listening for connection from client..")

        def server_thread():
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.bind((self.server_ip, int(self.port)))
            self.server.listen(1)
            self.client = self.server.accept()

            self.label.setText(self.label.text() + f"\n Accepted connection from client. Say Hi!")
            self.can_use = True
            while True:
                data = self.client.recv(1024).decode()
                self.receive_message(data)

        threading.Thread(target=server_thread, daemon=True).start()

    def createClient(self):
        if self.is_Server or self.is_Client:
            return
        
        self.is_Client = True

        def client_thread():
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect((self.server_ip, int(self.port)))
            self.label.setText(self.label.text() + f"\n Searching for server @ port {self.port}")
            self.window.setWindowTitle("Client @Port: " + self.port)
            self.label.setText(self.label.text() + f"\n Accepted connection from server. Say Hi!")
            self.can_use = True
            while True:
                data = self.client.recv(1024).decode()
                self.receive_message(data)

        threading.Thread(target=client_thread, daemon=True).start()

    def send_message(self):
        if not self.can_use:
            return
        
        self.label.setText(self.label.text() + f"\n You: {self.textbox.text()}")
        self.client.send(self.textbox.text().encode())
        self.textbox.clear()

    def receive_message(self, contents):
        self.label.setText(self.label.text() + f"\n Other: {contents}")

    def start(self):
        self.serverButton.clicked.connect(self.createServer)
        self.clientButton.clicked.connect(self.createClient)
        self.textbox.returnPressed.connect(self.send_message)

        self.window.show()
        
        sys.exit(self.app.exec_())

app = SocketMessage()

app.start()
