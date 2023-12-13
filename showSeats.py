from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout, QVBoxLayout, QMenuBar, QAction, QTableWidget, QTableWidgetItem, QMessageBox
from PyQt5.QtGui import QIcon, QColor 
from PyQt5.QtCore import QSize, Qt
from data import filmList
import json
from ticketSales import ticketSalesScreen

class showSeats(QWidget):
    def __init__(self, film):
        super().__init__() 

        # Set window and properties
        self.setWindowIcon(QIcon('icons/film.png'))
        self.film = film
        self.choosenSeats = []
        self.setGeometry(300, 200, 1600, 800)
        self.setWindowTitle((self.film.filmName))

        # Create the seat view and menu
        self.seatView()
        self.createMenu()

    def seatView(self):
        # Set up the main layout and grid for seat buttons
        layout = QVBoxLayout()
        self.grid = QGridLayout()

        # Iterate through each seat in the film
        for seat in self.film.seatInfo:
            seatNo = seat.seatNo
            seatOccupied = seat.seatOccupied

            # Create a button for each seat
            button = QPushButton(f"{seatNo}")
            button.setFixedSize(QSize(160, 80))
            button.clicked.connect(self.chooseSeatsCall(seatNo))

            # Set button properties based on seat occupancy
            if seatOccupied:
                button.setEnabled(False)
                button.setStyleSheet("background-color: red; color: black; border-radius: 10px;")
            else:
                button.setEnabled(True)
                button.setStyleSheet("background-color: green; color: white; border-radius: 10px;")
            # Add the button to the grid
            row, col = divmod(seatNo-1, 5)
            self.grid.addWidget(button, row, col)

        # Create buy and clean buttons
        self.buyButton = QPushButton("Buy the choosen tickets.")
        self.buyButton.setFixedSize(QSize(500, 70))
        self.buyButton.setStyleSheet("background-color: gray; color:white; border-radius: 10px; font-size: 20px")
        self.buyButton.clicked.connect(self.buyTickets) #Connected buyTickets function, which leads us ticketSales screen
        self.buyButton.setEnabled(False)

        self.cleanButton = QPushButton("Clean the seats.")
        self.cleanButton.setFixedSize(QSize(500, 70))
        self.cleanButton.setStyleSheet("background-color: red; color: white; border-radius: 10px; font-size: 20px")
        self.cleanButton.clicked.connect(self.cleanTheSeats) #Connected cleanTheSeats cleans up all tables for new session

        # Add the grid and buttons to the main layout
        layout.addLayout(self.grid)
        layout.addWidget(self.buyButton, alignment = Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.cleanButton, alignment = Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)
    
    def chooseSeatsCall(self, seatNo):
        # Return a callback function for the button click event
        def chooseSeats():
            choosenSeatNo = self.grid.itemAt(seatNo - 1).widget()
            if seatNo not in self.choosenSeats:
                # Add the chosen seat to the list
                self.choosenSeats.append(seatNo)
                choosenSeatNo.setStyleSheet("background-color: orange; color: black; border-radius: 10px;")
                if len(self.choosenSeats) == 1:
                    # Enable buy button when at least one seat is chosen
                    self.buyButton.setStyleSheet("background-color: green; color: white; border-radius: 10px; font-size: 20px")
                    self.buyButton.setEnabled(True)
            else:
                # Remove the chosen seat from the list
                self.choosenSeats.remove(seatNo)
                choosenSeatNo.setStyleSheet("background-color: green; color: white; border-radius: 10px;")
                if len(self.choosenSeats) == 0:
                    # Disable buy button when no seats are chosen
                    self.buyButton.setStyleSheet("background-color: gray; color:white; border-radius: 10px; font-size: 20px")
                    self.buyButton.setEnabled(False)
        return chooseSeats
    
    def buyTickets(self):
        # Close the current window and open the ticket sales screen
        self.close()
        self.buyTicket = ticketSalesScreen(film = self.film, choosenSeats = self.choosenSeats)
        self.buyTicket.show()

    def cleanTheSeats(self):
        # Display a message and clean occupied seats when the film session is over
        QMessageBox.information(self, "Attention!!!", "Please note that you can clean seat information only when the current film session is over.")
        jsonFile = open("rawData.json", "r") #open the file
        jsonData = json.load(jsonFile) #get the data
        jsonFile.close() #close the file
        
        # Use loop for cleaning up all seat registrations
        for seat in range(len(self.film.seatInfo)):
            jsonData[f"{self.film.filmName}"]['seatInfo'][seat - 1]['seatOccupied'] = 0
            jsonData[f"{self.film.filmName}"]['seatInfo'][seat - 1]['buyerName'] = ""
            jsonData[f"{self.film.filmName}"]['seatInfo'][seat - 1]['amount'] = 0
        
            id = self.film.id
            filmList[id - 1].seatInfo[seat - 1].seatOccupied = 0
            filmList[id - 1].seatInfo[seat - 1].buyerName = ""
            filmList[id - 1].seatInfo[seat - 1].amount = 0


            self.close()
            

        jsonFile = open('rawData.json', "w") # Open json file again
        jsonFile.write(json.dumps(jsonData, indent = 4)) # Put new cleaned data on it
        jsonFile.close() # Close the date

    # Create shortcut for occupied seats information 
    def createMenu(self):
        menuBar = QMenuBar(self)
        detailMenu = menuBar.addMenu("Details")

        showTicketsAction = QAction("Show the tickets", self)
        showTicketsAction.setShortcut("Ctrl+I")
        showTicketsAction.triggered.connect(self.showOccupiedSeats)

        detailMenu.addAction(showTicketsAction)


    def showOccupiedSeats(self):
        # Create a separate window to display occupied seats information
        self.window = QWidget()
        self.window.setWindowTitle("Ticket info.")
        self.window.setFixedSize(QSize(800, 800))

        # Find occupied seats and create a table to display the information
        occupiedSeats = self.findOccupiedSeats()
        showSeatsTable = QTableWidget(self.window)
        showSeatsTable.setRowCount(len(occupiedSeats) + 1)
        showSeatsTable.setColumnCount(3)
        showSeatsTable.setFixedSize(800, 800)

        #Menu header 
        seatNoHeader = QTableWidgetItem("Seat no")
        seatNoHeader.setBackground(QColor(255, 0, 0))
        showSeatsTable.setItem(0, 0, seatNoHeader)
        
        seatBuyerNameHeader = QTableWidgetItem("Buyer name")
        seatBuyerNameHeader.setBackground(QColor(255, 0, 0))
        showSeatsTable.setItem(0, 1, seatBuyerNameHeader)

        
        seatPaidAmountHeader = QTableWidgetItem("Ticket price")
        seatPaidAmountHeader.setBackground(QColor(255, 0, 0))
        showSeatsTable.setItem(0, 2, seatPaidAmountHeader)

        #Menu rows 
        for index, seat in enumerate(occupiedSeats):
            showSeatsTable.setItem(index + 1, 0, QTableWidgetItem(str(seat.seatNo)))
            showSeatsTable.setItem(index + 1, 1, QTableWidgetItem(str(seat.buyerName)))
            showSeatsTable.setItem(index + 1, 2, QTableWidgetItem(str(seat.amount)))

        self.window.show()

    def findOccupiedSeats(self):
        # Find and return occupied seats for the current film
        occupiedSeats = []
        id = self.film.id
        for seat in filmList[id-1].seatInfo:
            if seat.seatOccupied == 1:
                occupiedSeats.append(seat)
        return occupiedSeats
