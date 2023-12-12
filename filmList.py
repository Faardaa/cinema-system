from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QSize
from data import filmList
from showSeats import showSeats

class showFilmList(QWidget):
    def __init__(self):
        super().__init__()
        #Set up windows things
        self.setWindowTitle("Cinema ticket")
        self.setWindowIcon(QIcon("icons/cinema.png"))
        self.setFixedSize(1600, 800)
        self.filmListUIO()

    def filmListUIO(self):
        # Set up a grid layout to display film posters
        grid = QGridLayout()

        # Iterate through each film in the filmList
        for index, film in enumerate(filmList):
            imageLink = film.imageLink

            # Load film poster image using QPixmap
            try:
                pixmap = QPixmap(f"FilmPosters/{imageLink}")
                if pixmap.isNull() :
                    raise Exception(f"Filed to load image: FilmPosters/{imageLink}")
            except Exception as e:
                Exception(f"Error loading image: {e}")

            # Create a button for each film with its poster as the icon
            button = QPushButton()
            button.setIcon(QIcon(pixmap))
            button.setIconSize(QSize(300, 300))
            button.setFixedSize(QSize(300, 300))
            button.setStyleSheet("background-color: black;")
            # Connect the button click event to the filmClickedCall method to show specific film screen 
            button.clicked.connect(self.filmClickedCall(film))

            row, col = divmod(index, 3)
            # Add the button to the grid layout
            grid.addWidget(button, row, col)
        self.setLayout(grid)
    def filmClickedCall(self, film):
        # Return a callback function for the button click event
        def filmClicked():
            # Open the showSeats screen for the selected film
            self.showSeats = showSeats(film)
            self.showSeats.show()
        return filmClicked
