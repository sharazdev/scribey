import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from view import MainWindow
from controller import Controller
from model import Model

def main():
    # Create the application
    app = QApplication(sys.argv)

    model = Model()
    view = MainWindow()
    controller = Controller(model, view)

    # Set up the controller for the view
    view.set_controller(controller)
    
    # Show the main window and start the event loop
    view.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()