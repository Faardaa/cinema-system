from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QMessageBox, QPushButton, QLabel, QLineEdit, QRadioButton, QFrame, QButtonGroup
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize

from data import filmList
import json

class ticketSalesScreen(QWidget):
    def __init__(self, film, choosenSeats):
        super().__init__()

        # Set the window icon
        self.setWindowIcon(QIcon("icons/cinema.png"))

        # Initialize class variables
        self.film = film
        self.choosenSeats = choosenSeats
        self.lineEditList = []
        self.ticketType = [] # False - Student; True - Full
        self.numOfChoosenSeats = len(self.choosenSeats)
        self.totalAmount = 0
        self.studentTicketPrice = 15
        self.fullTicketPrice = 20
        dynamicHeight = 180 * self.numOfChoosenSeats

        # Set window properties
        self.setWindowTitle(f"Buy {film.filmName} tickets")
        self.setFixedSize(400, dynamicHeight)

        # Create the ticket sales form
        self.createForm()

    def createForm(self):
        layout = QVBoxLayout()
        self.totalAmountLabel = QLabel(f"Total amount: {self.totalAmount}")

        # Iterate over the chosen seats
        for seatNo in self.choosenSeats:
            seatNoLabel = QLabel(f"Seat number:{seatNo}")
            layout.addWidget(seatNoLabel)

            # Add user data input fields
            hBoxUserData = QHBoxLayout()
            nameSurnameLabel = QLabel(f"Name and surname:")
            nameSurnameLineEdit = QLineEdit()
            self.lineEditList.append(nameSurnameLineEdit)
            hBoxUserData.addWidget(nameSurnameLabel)
            hBoxUserData.addWidget(nameSurnameLineEdit)
            layout.addLayout(hBoxUserData)

            # Add radio buttons for ticket type selection
            hRadioButtonLayout = QHBoxLayout()
            fullPriceTRB = QRadioButton(f"Full ticket.")
            studentPriceTRB = QRadioButton(f"Student ticket.")
            buttonGroup = QButtonGroup(self)
            buttonGroup.addButton(fullPriceTRB)
            buttonGroup.addButton(studentPriceTRB)
            buttonGroup.buttonToggled.connect(self.ticketTypeForSeat)
            hRadioButtonLayout.addWidget(fullPriceTRB)
            hRadioButtonLayout.addWidget(studentPriceTRB)
            layout.addLayout(hRadioButtonLayout)

            # Add a line separator
            line = QFrame(frameShape=QFrame.HLine)
            layout.addWidget(line)

        layout.addWidget(self.totalAmountLabel)

        # Add a button to buy the tickets
        self.buyTicketsButton = QPushButton("Buy the tickets.")
        self.buyTicketsButton.clicked.connect(self.buyTicketsClicked)
        layout.addWidget(self.buyTicketsButton)

        # Set the layout for the widget
        self.setLayout(layout)

    def ticketTypeForSeat(self, button, checked):
        # Update total amount based on selected ticket type
        if checked and "Student" in button.text():
            self.totalAmount += self.studentTicketPrice
            self.ticketType.append(False)
        elif checked and "Full" in button.text():
            self.totalAmount += self.fullTicketPrice
            self.ticketType.append(True)
        self.totalAmountLabel.setText(f"Total amount: {self.totalAmount}")

    def buyTicketsClicked(self):
        # Check if all required information is provided
        if len(self.ticketType) != self.numOfChoosenSeats:
                QMessageBox.warning(self, "Missing information!!!", "Please submit your ticket type.")
                return
        for lineEdit in self.lineEditList:
            if len(lineEdit.text()) == 0:
                QMessageBox.warning(self, "Missing information!!!", "Please enter your name and surname.")
                return
        userAnswer = QMessageBox.question(self, "Confirmation", f"Total amount: {self.totalAmount} \n\nAre you sure you want to buy tickets?", QMessageBox.Yes | QMessageBox.No)
        # Confirm ticket purchase
        if userAnswer == QMessageBox.Yes:
            self.ticketSold()

    def ticketSold(self):
        # Update seat information in the database and film list
        jsonFile = open("rawData.json", "r") #open the file
        jsonData = json.load(jsonFile) #get the data
        jsonFile.close() #close the file

        for index, lineEdit in enumerate(self.lineEditList):
            choosenSeatNo = self.choosenSeats[index]

            jsonData[f"{self.film.filmName}"]['seatInfo'][choosenSeatNo-1]['seatOccupied'] = 1 # Make it occupied 
            jsonData[f"{self.film.filmName}"]['seatInfo'][choosenSeatNo - 1]['buyerName'] = lineEdit.text()  # Set buyers name 
            if self.ticketType[index]: # Set proper price of it
                jsonData[f"{self.film.filmName}"]['seatInfo'][choosenSeatNo - 1]['amount'] = self.fullTicketPrice
            else:
                jsonData[f"{self.film.filmName}"]['seatInfo'][choosenSeatNo - 1]['amount'] = self.studentTicketPrice

            # To see directly result we have to update same data in our data list
            id = self.film.id
            filmList[id - 1].seatInfo[choosenSeatNo - 1].seatOccupied = 1
            filmList[id - 1].seatInfo[choosenSeatNo - 1].buyerName = lineEdit.text()
            if self.ticketType[index]:
                filmList[id - 1].seatInfo[choosenSeatNo - 1].amount = self.fullTicketPrice
            else:
                filmList[id - 1].seatInfo[choosenSeatNo - 1].amount = self.studentTicketPrice

        # Save the updated information to the database
        jsonFile = open('rawData.json', "w")
        jsonFile.write(json.dumps(jsonData, indent = 4))
        jsonFile.close()

        # Display a success message
        QMessageBox.information(self, "Success", "The purchasing process completed successfully")
        self.close()