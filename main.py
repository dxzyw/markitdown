import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, QTextEdit, 
                            QVBoxLayout, QHBoxLayout, QWidget, QFileDialog, QLabel)
from PyQt6.QtCore import Qt
from markitdown import MarkItDown

class MarkItDownGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MarkItDown Converter")
        self.setMinimumSize(600, 400)
        
        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        # Instructions
        instructions = QLabel(
            "Instructions:\n"
            "1. Click 'Open File' to select a document (PDF, DOCX, etc.)\n"
            "2. Click 'Convert' to transform it to Markdown\n"
            "3. The result will appear in the text area below\n"
            "4. Click 'Save' to save the Markdown content"
        )
        instructions.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(instructions)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.open_btn = QPushButton("Open File")
        self.open_btn.clicked.connect(self.open_file)
        button_layout.addWidget(self.open_btn)
        
        self.convert_btn = QPushButton("Convert")
        self.convert_btn.clicked.connect(self.convert_file)
        self.convert_btn.setEnabled(False)
        button_layout.addWidget(self.convert_btn)
        
        self.save_btn = QPushButton("Save")
        self.save_btn.clicked.connect(self.save_file)
        self.save_btn.setEnabled(False)
        button_layout.addWidget(self.save_btn)
        
        layout.addLayout(button_layout)
        
        # Status label
        self.status_label = QLabel("")
        layout.addWidget(self.status_label)
        
        # Text area
        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)
        layout.addWidget(self.text_area)
        
        self.file_path = None
        self.markdown_content = None

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Document",
            "",
            "Documents (*.pdf *.docx *.doc *.pptx *.xlsx);;All Files (*.*)"
        )
        
        if file_path:
            self.file_path = file_path
            self.status_label.setText(f"Selected file: {file_path}")
            self.convert_btn.setEnabled(True)
            self.save_btn.setEnabled(False)
            self.text_area.clear()

    def convert_file(self):
        if not self.file_path:
            return
            
        try:
            self.status_label.setText("Converting...")
            QApplication.processEvents()
            
            with open(self.file_path, 'rb') as f:
                content = f.read()
            
            md = MarkItDown()
            result = md.convert(content)
            self.markdown_content = result.text_content
            
            self.text_area.setText(self.markdown_content)
            self.status_label.setText("Conversion completed!")
            self.save_btn.setEnabled(True)
            
        except Exception as e:
            self.status_label.setText(f"Error: {str(e)}")

    def save_file(self):
        if not self.markdown_content:
            return
            
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Markdown",
            "",
            "Markdown Files (*.md);;All Files (*.*)"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(self.markdown_content)
                self.status_label.setText(f"Saved to: {file_path}")
            except Exception as e:
                self.status_label.setText(f"Error saving file: {str(e)}")

def main():
    app = QApplication(sys.argv)
    window = MarkItDownGUI()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()