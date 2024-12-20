import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, QTextEdit, 
                            QVBoxLayout, QHBoxLayout, QWidget, QFileDialog, QLabel,
                            QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon
from markitdown import MarkItDown

class MarkItDownGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Initialize the UI"""
        self.setWindowTitle("MarkItDown")
        self.setMinimumSize(500, 400)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QPushButton {
                padding: 8px 15px;
                background-color: #0078d4;
                color: white;
                border: none;
                border-radius: 4px;
                min-width: 100px;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
            QLabel {
                color: #333333;
            }
            QTextEdit {
                border: 1px solid #cccccc;
                border-radius: 4px;
                padding: 8px;
                background-color: white;
            }
        """)
        
        # Main layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Welcome message
        welcome = QLabel("Welcome to MarkItDown")
        welcome.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        welcome.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(welcome)
        
        # Quick guide
        guide = QLabel(
            "Quick Guide:\n"
            "① Select a document (PDF, Word, etc.)\n"
            "② Convert to Markdown\n"
            "③ Save the result"
        )
        guide.setFont(QFont("Arial", 10))
        guide.setAlignment(Qt.AlignmentFlag.AlignLeft)
        guide.setStyleSheet("padding: 10px; background-color: #e6f3ff; border-radius: 4px;")
        layout.addWidget(guide)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        self.open_btn = QPushButton("Select File")
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
        self.status_label.setStyleSheet("color: #666666;")
        layout.addWidget(self.status_label)
        
        # Text area
        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)
        self.text_area.setPlaceholderText("Converted markdown will appear here...")
        layout.addWidget(self.text_area)
        
        self.file_path = None
        self.markdown_content = None

    def open_file(self):
        """Handle file selection"""
        try:
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "Select Document",
                "",
                "Documents (*.pdf *.docx *.doc *.pptx *.xlsx);;All Files (*.*)"
            )
            
            if file_path:
                # 检查文件大小
                file_size = os.path.getsize(file_path)
                max_size = 100 * 1024 * 1024  # 100MB
                
                if file_size > max_size:
                    raise Exception(f"File is too large (max size: 100MB)")
                
                # 检查文件类型
                ext = os.path.splitext(file_path)[1].lower()
                supported_types = ['.pdf', '.docx', '.doc', '.pptx', '.xlsx']
                
                if ext not in supported_types:
                    raise Exception(f"Unsupported file type: {ext}")
                
                self.file_path = file_path
                self.status_label.setText(f"Selected: {file_path}")
                self.convert_btn.setEnabled(True)
                self.save_btn.setEnabled(False)
                self.text_area.clear()
                
        except Exception as e:
            self.show_error("File Selection Error", str(e))
            self.file_path = None
            self.convert_btn.setEnabled(False)

    def convert_file(self):
        """Convert the selected file to markdown using basic MarkItDown functionality"""
        if not self.file_path:
            return
        
        try:
            self.status_label.setText("Converting...")
            self.convert_btn.setEnabled(False)
            QApplication.processEvents()
            
            # 使用基本的 MarkItDown 转换
            md = MarkItDown()
            result = md.convert(self.file_path)  # 直接传入文件路径
            
            if not result or not hasattr(result, 'text_content'):
                raise Exception("Conversion failed. Please try another file.")
            
            self.markdown_content = result.text_content
            
            # 显示结果
            self.text_area.setText(self.markdown_content)
            self.status_label.setText("✓ Conversion completed!")
            self.save_btn.setEnabled(True)
            
        except Exception as e:
            self.show_error("Conversion Error", str(e))
            self.markdown_content = None
            self.text_area.clear()
            self.save_btn.setEnabled(False)
        finally:
            self.convert_btn.setEnabled(True)

    def show_error(self, title, message):
        """Show simple error message"""
        QMessageBox.critical(self, title, str(message))
        self.status_label.setText(f"Error: {message}")

    def save_file(self):
        """Save the converted markdown"""
        if not self.markdown_content:
            return
            
        try:
            suggested_name = self.file_path.rsplit('.', 1)[0] + '.md'
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Save Markdown",
                suggested_name,
                "Markdown Files (*.md);;All Files (*.*)"
            )
            
            if file_path:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(self.markdown_content)
                self.status_label.setText(f"✓ Saved to: {file_path}")
        except Exception as e:
            self.show_error("Save Error", str(e))

def main():
    try:
        app = QApplication(sys.argv)
        app.setStyle('Fusion')  # 使用 Fusion 风格获得更现代的外观
        window = MarkItDownGUI()
        window.show()
        sys.exit(app.exec())
    except Exception as e:
        QMessageBox.critical(None, "Fatal Error", f"Application Error: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()