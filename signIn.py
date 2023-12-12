from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLineEdit, QMessageBox, QLabel, QDateEdit, QPushButton
from PyQt5.QtCore import QSize, QDate, Qt
from PyQt5.QtGui import QIcon, QKeySequence
import hashlib
from userDatabase import DatabaseSignIn

class signIn(QWidget):  
    def __init__(self):
        super().__init__()

        # Set up the main vertical layout
        vBox = QVBoxLayout()

        # Set window properties
        self.setWindowTitle("Log in")
        self.setFixedSize(QSize(400, 450))
        self.setWindowIcon(QIcon("icons/logIn.png"))

        # Create first name layout, label and lineEdit to get first name
        hBoxName = QHBoxLayout()
        self.nameLabel = QLabel("First name:")
        self.nameLineEdit = QLineEdit()
        self.nameLineEdit.setFixedSize(210, 30)
        hBoxName.addWidget(self.nameLabel)
        hBoxName.addWidget(self.nameLineEdit)
        hBoxName.setContentsMargins(0, 10, 0, 10)

        # Create last name layout, label and lineEdit to get last name
        hBoxLastName = QHBoxLayout()
        self.lastNameLabel = QLabel("Last name:")
        self.lastNameLineEdit = QLineEdit()
        self.lastNameLineEdit.setFixedSize(210, 30)
        hBoxLastName.addWidget(self.lastNameLabel)
        hBoxLastName.addWidget(self.lastNameLineEdit)
        hBoxLastName.setContentsMargins(0, 10, 0, 10)

        # Create birth date layout, label and dateEdit to get birtheday
        hBoxBirthDate = QHBoxLayout()
        self.birthDateLabel = QLabel("Birth date:")
        self.birthDateLineEdit = QDateEdit(self)
        self.birthDateLineEdit.setCalendarPopup(True)  # Enable the popup calendar
        self.birthDateLineEdit.setDateRange(QDate(1900, 1, 1), QDate.currentDate())  # Set a reasonable date range
        self.birthDateLineEdit.setFixedSize(210, 30)
        hBoxBirthDate.addWidget(self.birthDateLabel)
        hBoxBirthDate.addWidget(self.birthDateLineEdit)
        hBoxBirthDate.setContentsMargins(0, 10, 0, 10)

        #Create user name layout, label and lineEdit to get user name
        hBoxUserName = QHBoxLayout()
        self.userNameLabel = QLabel("User name:")
        self.userNameLineEdit = QLineEdit()
        self.userNameLineEdit.setMaxLength(20)
        self.userNameLineEdit.setFixedSize(210, 30)
        hBoxUserName.addWidget(self.userNameLabel)
        hBoxUserName.addWidget(self.userNameLineEdit)
        hBoxUserName.setContentsMargins(0, 10, 0, 10)

        # Create password layout, label and lineEdit to get pass
        hBoxPassword = QHBoxLayout()
        self.passwordLabel = QLabel("Password:")
        self.passwordLineEdit = QLineEdit()
        self.passwordLineEdit.setEchoMode(QLineEdit.Password)
        self.passwordLineEdit.setFixedSize(175, 30)

        # Button to show password
        self.showPassButton = QPushButton()
        self.showPassButton.setFixedSize(30, 30)
        self.showPassButton.setIcon(QIcon('icons/hideThePass.png'))
        self.showPassButton.setCheckable(True)
        self.showPassButton.clicked.connect(self.passwordVisibility)

        # Add show pass widgets to the layout
        hBoxPassword.addWidget(self.passwordLabel)
        hBoxPassword.addWidget(self.passwordLineEdit)
        hBoxPassword.addWidget(self.showPassButton)
        hBoxPassword.setContentsMargins(0, 10, 0, 10)

        # Getting password second time to check are they same 
        hBoxPassword2 = QHBoxLayout()
        self.passwordLabel2 = QLabel("Submit your password:")
        self.passwordLineEdit2 = QLineEdit()
        self.passwordLineEdit2.setEchoMode(QLineEdit.Password)
        self.passwordLineEdit2.setFixedSize(175, 30)

        self.showPassButton2 = QPushButton()
        self.showPassButton2.setFixedSize(30, 30)
        self.showPassButton2.setIcon(QIcon('icons/hideThePass.png'))
        self.showPassButton2.setCheckable(True)
        self.showPassButton2.clicked.connect(self.passwordVisibility)

        hBoxPassword2.addWidget(self.passwordLabel2)
        hBoxPassword2.addWidget(self.passwordLineEdit2)
        hBoxPassword2.addWidget(self.showPassButton2)
        hBoxPassword2.setContentsMargins(0, 10, 0, 10)

        # Add some confirm button
        self.confirmButton = QPushButton()
        self.confirmButton.setText("Sign in")
        self.confirmButton.setFixedSize(120, 40)
        self.confirmButton.clicked.connect(self.submit_sign_in)
        self.confirmButton.setShortcut(QKeySequence("Return"))

        # Add all the horizontal layouts to the vBox layout
        vBox.addLayout(hBoxName)
        vBox.addLayout(hBoxLastName)
        vBox.addLayout(hBoxBirthDate)
        vBox.addLayout(hBoxUserName)
        vBox.addLayout(hBoxPassword)
        vBox.addLayout(hBoxPassword2)
        vBox.addWidget(self.confirmButton, alignment = Qt.AlignmentFlag.AlignCenter)

        # And set vBox layout as main of the window
        self.setLayout(vBox)


    def passwordVisibility(self):
        # Toggle password visibility based on the clicked button
        clicked_button = self.sender()
        if clicked_button == self.showPassButton : 
            if clicked_button.isChecked():
                self.passwordLineEdit.setEchoMode(QLineEdit.Normal)
                self.showPassButton.setIcon(QIcon('icons/showThePass.png'))
            else:
                self.passwordLineEdit.setEchoMode(QLineEdit.Password)
                self.showPassButton.setIcon(QIcon('icons/hideThePass.png'))

        elif clicked_button == self.showPassButton2:
            if clicked_button.isChecked():
                self.passwordLineEdit2.setEchoMode(QLineEdit.Normal)
                self.showPassButton2.setIcon(QIcon('icons/showThePass.png'))
            else:
                self.passwordLineEdit2.setEchoMode(QLineEdit.Password)
                self.showPassButton2.setIcon(QIcon('icons/hideThePass.png'))

    # Hash the provided password using SHA-256
    def hash_password(self, password):          
            # Create a new SHA-256 hash object
            sha256_hash = hashlib.sha256()

            # Update the hash object with the password bytes
            sha256_hash.update(password.encode('utf-8'))

            # Get the hexadecimal representation of the hash
            hashed_password = sha256_hash.hexdigest()

            return hashed_password
    
    def submit_sign_in(self):
        # Check if any of the required fields are empty
        if any(value is None or value == '' for value in [self.nameLineEdit.text(), self.lastNameLineEdit.text(), self.passwordLineEdit.text(), self.passwordLineEdit2.text()]):
            QMessageBox.critical(self, "Sign-in Failed", "Please fill in all the fields.")
            return

        # Check if the (hashed) passwords are match
        if self.passwordLineEdit.text() != self.passwordLineEdit2.text():
            QMessageBox.critical(self, "Sign-in Failed", "Passwords do not match. Please make sure both password fields are the same.")
            self.passwordLineEdit.clear()
            self.passwordLineEdit2.clear()
            return
        
        # Check password strength
        if not any(char.isupper() for char in self.passwordLineEdit.text()):  # At least one uppercase letter
            QMessageBox.critical(self, "Sign-in Failed", "Password must contain at least one uppercase letter.")
            return
        if not any(char.islower() for char in self.passwordLineEdit.text()):  # At least one lowercase letter
            QMessageBox.critical(self, "Sign-in Failed", "Password must contain at least one lowercase letter.")
            return
        if not any(char.isdigit() for char in self.passwordLineEdit.text()):  # At least one digit
            QMessageBox.critical(self, "Sign-in Failed", "Password must contain at least one digit.")
            return
        if not any(char in "!@#$%^&*()-_=+[]{}|;:'\",.<>?/" for char in self.passwordLineEdit.text()):  # At least one special character
            QMessageBox.critical(self, "Sign-in Failed", "Password must contain at least one special character.")
            return

        # Hash the password
        hashed_pass = self.hash_password(self.passwordLineEdit.text())

        # Prepare user sign-in information        
        self.userSignInInfo = {
        'name' : self.nameLineEdit.text(),
        'surname' : self.lastNameLineEdit.text(),
        'birthdate' : self.birthDateLineEdit.text(),
        'username' : self.userNameLineEdit.text(),
        'password' : hashed_pass}

        # Send the sign-in information to the database
        self.userDatabase = DatabaseSignIn(self.userSignInInfo)

        # Display a success message        
        QMessageBox.information(self, "New accound.", "Accound have been created successfully.")
        self.close()