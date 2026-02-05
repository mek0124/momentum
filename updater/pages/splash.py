from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QProgressBar, QPushButton
)
from PySide6.QtCore import Qt, QTimer
import subprocess
import sys
from pathlib import Path

from ..utils.update_thread import UpdateThread


class SplashScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("SplashScreen")
        
        self.parent_window = parent
        self.color_theme = parent.color_theme
        self.root_dir = parent.root_dir
        self.latest_version = parent.latest_version
        
        self.update_thread = None
        self.progress_timer = None
        
        self.setup_ui()
        self.apply_styles()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(30)
        layout.setAlignment(Qt.AlignCenter)
        
        title_label = QLabel("Updating Momentum")
        title_label.setAlignment(Qt.AlignCenter)
        self.title_label = title_label
        
        self.status_label = QLabel("Preparing update...")
        self.status_label.setAlignment(Qt.AlignCenter)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        
        self.details_label = QLabel("")
        self.details_label.setAlignment(Qt.AlignCenter)
        self.details_label.setWordWrap(True)
        
        self.file_label = QLabel("")
        self.file_label.setAlignment(Qt.AlignCenter)
        self.file_label.setWordWrap(True)
        
        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(20)
        button_layout.setAlignment(Qt.AlignCenter)
        
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setFixedSize(120, 40)
        self.cancel_button.clicked.connect(self.cancel_update)
        
        self.restart_button = QPushButton("Restart App")
        self.restart_button.setFixedSize(120, 40)
        self.restart_button.clicked.connect(self.restart_application)
        self.restart_button.setVisible(False)
        
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.restart_button)
        
        layout.addWidget(title_label)
        layout.addWidget(self.status_label)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.details_label, 1)
        layout.addWidget(self.file_label)
        layout.addWidget(button_container)
        layout.addStretch()
    
    def apply_styles(self):
        self.setStyleSheet(
            f"""
                QLabel {{
                    color: {self.color_theme['text_primary']};
                    font-size: 14px;
                }}
                
                QLabel#title {{
                    font-size: 24px;
                    font-weight: bold;
                    color: {self.color_theme['primary']};
                }}
                
                QProgressBar {{
                    border: 2px solid {self.color_theme['primary']};
                    border-radius: {self.color_theme['border_radius_medium']};
                    text-align: center;
                    height: 25px;
                    background-color: {self.color_theme['surface']};
                }}
                
                QProgressBar::chunk {{
                    background-color: {self.color_theme['primary']};
                    border-radius: {self.color_theme['border_radius_medium']};
                }}
                
                QPushButton {{
                    border: 2px solid {self.color_theme['primary']};
                    border-radius: {self.color_theme['border_radius_medium']};
                    background-color: transparent;
                    color: {self.color_theme['primary']};
                    font-size: 14px;
                }}
                
                QPushButton:hover {{
                    background-color: {self.color_theme['surface_light']};
                }}
                
                QPushButton:pressed {{
                    background-color: {self.color_theme['primary']};
                    color: black;
                }}
            """
        )
        self.title_label.setObjectName("title")
    
    def start_update(self):
        self.update_thread = UpdateThread(self.root_dir, self.latest_version)
        self.update_thread.progress_update.connect(self.update_progress)
        self.update_thread.finished.connect(self.update_finished)
        
        self.start_smooth_progress()
        self.update_thread.start()
    
    def start_smooth_progress(self):
        self.progress_timer = QTimer()
        self.progress_timer.timeout.connect(self.increment_progress)
        self.progress_timer.start(50)
    
    def increment_progress(self):
        current_value = self.progress_bar.value()
        if current_value < 100:
            new_value = current_value + 1
            self.progress_bar.setValue(new_value)
            
            if new_value < 10:
                self.status_label.setText("Initializing update...")
                self.details_label.setText("Setting up update environment...")
            elif new_value < 30:
                self.status_label.setText("Preparing download...")
                self.details_label.setText("Connecting to GitHub...")
            elif new_value < 60:
                self.status_label.setText("Processing files...")
                self.details_label.setText("Getting ready to apply updates...")
            elif new_value < 90:
                self.status_label.setText("Finalizing...")
                self.details_label.setText("Almost done...")
            elif new_value < 95:
                self.status_label.setText("Almost complete...")
                self.details_label.setText("Finishing up...")
        else:
            if self.progress_timer:
                self.progress_timer.stop()
    
    def update_progress(self, status, value):
        if self.progress_timer:
            self.progress_timer.stop()
        
        self.progress_bar.setValue(value)
        self.status_label.setText(status)
        
        if "Updating" in status or "Adding" in status or "Removing" in status:
            self.file_label.setText(f"Current file: {status.split('...')[0]}")
        else:
            self.file_label.setText("")
        
        if value < 10:
            self.details_label.setText("Preparing update environment...")
        elif value < 30:
            self.details_label.setText("Downloading new version from GitHub...")
        elif value < 40:
            self.details_label.setText("Extracting update package...")
        elif value < 50:
            self.details_label.setText("Analyzing changes between versions...")
        elif value < 60:
            self.details_label.setText("Creating backup of modified files...")
        elif value < 90:
            self.details_label.setText("Applying updates to modified files...")
        else:
            self.details_label.setText("Finalizing installation...")
        
        if value < 100:
            self.start_smooth_progress()
    
    def update_finished(self, success, message):
        if self.progress_timer:
            self.progress_timer.stop()
        
        self.progress_bar.setValue(100)
        
        if success:
            self.status_label.setText("Update Complete!")
            self.details_label.setText(message)
            self.file_label.setText("")
            self.cancel_button.setVisible(False)
            self.restart_button.setVisible(True)
        else:
            self.status_label.setText("Update Failed!")
            self.details_label.setText(f"Error: {message}")
            self.file_label.setText("The application will restart with the previous version.")
            QTimer.singleShot(3000, self.restart_application)
    
    def cancel_update(self):
        if self.progress_timer:
            self.progress_timer.stop()
        
        if self.update_thread and self.update_thread.isRunning():
            self.update_thread.terminate()
            self.update_thread.wait()
        self.restart_application()
    
    def restart_application(self):
        main_script = self.root_dir / "main.py"
        subprocess.Popen([sys.executable, str(main_script)])
        from PySide6.QtWidgets import QApplication
        QApplication.quit()