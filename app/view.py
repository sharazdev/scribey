from PyQt5.QtWidgets import QMainWindow, QMessageBox, QFileDialog
from app_ui import Ui_MainWindow
import os

class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Handle the UI setup and user interactions.
    """

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.controller = None
        
        # Initially hide the new transcription button
        self.newTranscriptionButton.hide()
        
        # Connect the page change signal
        self.pagesStackedWidget.currentChanged.connect(self.on_page_changed)

    def set_controller(self, controller):
        """Set the controller for this view and connect signals"""
        self.controller = controller
        self.connect_signals()

    def connect_signals(self):
        """Connect UI element signals to controller slots"""
        self.homeBrowseButton.clicked.connect(self.controller.browse_file)
        self.newTranscriptionButton.clicked.connect(self.controller.new_transcription)
        self.fileTypeComboBox.currentIndexChanged.connect(self.controller.update_file_type)
        self.pushButton.clicked.connect(self.controller.download_transcription)

    def show_transcribe_page(self):
        """Display the transcription progress page"""
        self.pagesStackedWidget.setCurrentIndex(1)
        self.transcribeProgressLabel.setText("Transcription in progress...")
        if self.controller.model.current_file:
            filename = os.path.basename(self.controller.model.current_file)
            if len(filename) > 37:
                self.audioFilenameLabel.setText(filename[:37] + "...")
            else:
                self.audioFilenameLabel.setText(filename)

    def show_transcription_result(self, transcription):
        """Display the transcription result page"""
        formatted_transcription = self.controller.model.get_formatted_transcription()
        self.transcriptionTextLabel.setText(formatted_transcription)
        self.pagesStackedWidget.setCurrentIndex(2)

    def show_error_message(self, message):
        """Display an error message dialog"""
        QMessageBox.critical(self, "Error", message)

    def show_success_message(self, message):
        """Display a success message dialog"""
        QMessageBox.information(self, "Success", message)

    def on_page_changed(self, index):
        """Handle page changes in the stacked widget"""
        # Show the new transcription button only on the result page (index 2)
        self.newTranscriptionButton.setVisible(index == 2)

    def get_save_file_name(self, file_type):
        """Open a file dialog for saving the transcription"""
        file_filter = "SRT Files (*.srt)" if file_type == "Captions (.SRT File)" else "Text Files (*.txt)"
        return QFileDialog.getSaveFileName(self, "Save File", "", file_filter)[0]

    def reset_ui(self):
        """Reset the UI to its initial state"""
        self.pagesStackedWidget.setCurrentIndex(0)
        self.transcriptionTextLabel.clear()
        self.audioFilenameLabel.clear()