import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QRadioButton, 
                               QWidget, QVBoxLayout)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Set window properties
        self.setWindowTitle("Custom Radio Button")
        self.setGeometry(100, 100, 300, 200)
        
        # Set black background for the main window
        self.setStyleSheet("QMainWindow { background-color: black; }")
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Create the radio button
        self.radio_button = QRadioButton("Custom Radio Button")
        
        # Apply custom styling
        radio_stylesheet = """
        QRadioButton {
            color: white;
            font-size: 16px;
            spacing: 10px;
        }
        
        QRadioButton::indicator {
            width: 20px;
            height: 20px;
            border-radius: 10px;
        }
        
        QRadioButton::indicator:unchecked {
            border: 2px solid white;
            background-color: transparent;
        }
        
        QRadioButton::indicator:checked {
            border: none;
            background-color: green;
        }
        """
        
        self.radio_button.setStyleSheet(radio_stylesheet)
        
        # Add radio button to layout
        layout.addWidget(self.radio_button)

def main():
    app = QApplication(sys.argv)
    
    # Optional: Set application-wide dark palette
    app.setStyle("Fusion")
    dark_palette = QPalette()
    dark_palette.setColor(QPalette.ColorRole.Window, Qt.GlobalColor.black)
    dark_palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
    app.setPalette(dark_palette)
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()