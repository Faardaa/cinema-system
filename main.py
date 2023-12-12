import sys
from PyQt5.QtWidgets import QApplication
from entry import EntryScreen

# Initialize the PyQt application
app = QApplication(sys.argv)

# Create an instance of the EntryScreen (the main window)
entryScreen = EntryScreen()

# Show the EntryScreen
entryScreen.show()

# Start the application event loop
sys.exit(app.exec_())