from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QMessageBox, QLabel
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon, QKeySequence
from filmList import showFilmList
from signIn import signIn
from userDatabase import DatabaseLogIn
import hashlib

class EntryScreen(QWidget):
    def __init__(self):
        super().__init__()

        # Window setup
        self.setWindowTitle("Ticket sellings")
        self.setWindowIcon(QIcon('icons/cinema.png'))
        self.setFixedSize(360, 240)

        # Vertical layout
        vBox = QVBoxLayout()

        # Username layout for get username
        hBoxUserName = QHBoxLayout()
        self.userNameLabel = QLabel("User name: ")
        self.userNameLineEdit = QLineEdit()
        self.userNameLineEdit.setFixedSize(QSize(236, 25))
        hBoxUserName.addWidget(self.userNameLabel)
        hBoxUserName.addWidget(self.userNameLineEdit)
        hBoxUserName.setContentsMargins(0, 10, 0, 10)

        # Password layout for get user pass
        hBoxPassword = QHBoxLayout()
        self.passwordLabel = QLabel("Password: ")
        self.passwordLineEdit = QLineEdit()
        self.passwordLineEdit.setFixedSize(QSize(206, 25))
        self.passwordLineEdit.setEchoMode(QLineEdit.Password)

        # Show password button
        self.showPassButton = QPushButton()
        self.showPassButton.setFixedSize(25, 25)
        self.showPassButton.setIcon(QIcon('icons/hideThePass.png'))
        self.showPassButton.setCheckable(True)
        self.showPassButton.clicked.connect(self.passwordVisibility)

        hBoxPassword.addWidget(self.passwordLabel)
        hBoxPassword.addWidget(self.passwordLineEdit)
        hBoxPassword.addWidget(self.showPassButton)
        hBoxPassword.setContentsMargins(0, 5, 0, 15)

        # Confirm and sign-in buttons
        self.confirmButton = QPushButton()
        self.confirmButton.setText("Log in")
        self.confirmButton.setFixedSize(100, 30)
        self.confirmButton.clicked.connect(self.enter)
        self.confirmButton.setShortcut(QKeySequence("Return"))

        self.signInButton = QPushButton()
        self.signInButton.setText("Sign in")
        self.signInButton.setFixedSize(100, 30)
        self.signInButton.clicked.connect(self.signIn)

        # Add thoose layouts and buttons to the vertical layout
        vBox.addLayout(hBoxUserName)
        vBox.addLayout(hBoxPassword)
        vBox.addWidget(self.confirmButton, alignment = Qt.AlignmentFlag.AlignCenter)
        vBox.addWidget(QLabel("Don't have an account?"), alignment = Qt.AlignmentFlag.AlignCenter)
        vBox.addWidget(self.signInButton, alignment = Qt.AlignmentFlag.AlignCenter)

        # Set the layout for the widget
        self.setLayout(vBox)
    
    # Toggle password visibility
    def passwordVisibility(self):
        clicked_button = self.sender()
        if clicked_button.isChecked():
            self.passwordLineEdit.setEchoMode(QLineEdit.Normal)
            self.showPassButton.setIcon(QIcon('icons/showThePass.png'))
        else:
            self.passwordLineEdit.setEchoMode(QLineEdit.Password)
            self.showPassButton.setIcon(QIcon('icons/hideThePass.png'))

    # Hash the password using SHA-256
    def hash_password(self, password):
        # Create a new SHA-256 hash object
        sha256_hash = hashlib.sha256()

        # Update the hash object with the password bytes
        sha256_hash.update(password.encode('utf-8'))

        # Get the hexadecimal representation of the hash
        hashed_password = sha256_hash.hexdigest()

        return hashed_password
    
    # Validate user credentials and proceed to the film list screen
    def enter(self):
        hashed_pass = self.hash_password(self.passwordLineEdit.text())
        self.dataBaseResult = DatabaseLogIn(self.userNameLineEdit.text(), hashed_pass)
        if self.dataBaseResult:
            self.close()
            self.filmListScrene = showFilmList()
            self.filmListScrene.show()
        else:
            QMessageBox.warning(self, "Unsuccessfull login", "Username or password is wrong.")

    def signIn(self):
        # Open the sign-in screen
        self.signInScene = signIn()
        self.signInScene.show()