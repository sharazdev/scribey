from PyQt5.QtWidgets import QFileDialog

class Controller:
    """
    Handle user inputs and updates the model and view accordingly.
    """

    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.current_file_type = "Captions (.SRT File)"
        
        self.connect_signals()

    def connect_signals(self):
        """Connect model signals to view slots"""
        self.model.transcription_started.connect(self.view.show_transcribe_page)
        self.model.transcription_complete.connect(self.view.show_transcription_result)

    def browse_file(self):
        """Handle file browsing and initiate transcription if valid file is selected"""
        file_name, _ = QFileDialog.getOpenFileName(
            self.view, 
            "Select Audio File", 
            "", 
            "Audio Files (*.wav *.mp3 *.mp2 *.aac *.flac *.m4a *.ogg *.opus)"
        )
        if file_name:
            self.process_selected_file(file_name)

    def process_selected_file(self, file_name):
        """Validate and process the selected audio file"""
        if self.model.validate_audio_file(file_name):
            self.model.perform_transcription(file_name)
        else:
            self.view.show_error_message("Invalid audio file selected.")

    def new_transcription(self):
        """Reset the model and view for a new transcription"""
        self.model.reset_transcription()
        self.view.pagesStackedWidget.setCurrentIndex(0)

    def update_file_type(self, index):
        """Update the current file type based on user selection"""
        self.current_file_type = self.view.fileTypeComboBox.currentText()

    def download_transcription(self):
        """Handle the transcription download process"""
        file_name = self.view.get_save_file_name(self.current_file_type)
        if file_name:
            self.save_transcription(file_name)

    def save_transcription(self, file_name):
        """Save the transcription to a file"""
        content = self.get_transcription_content()
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(content)
        self.view.show_success_message("File saved successfully!")

    def get_transcription_content(self):
        """Get the appropriate transcription content based on the selected file type"""
        if self.current_file_type == "Captions (.SRT File)":
            return self.model.generate_srt()
        else:
            return self.model.get_formatted_transcription() 