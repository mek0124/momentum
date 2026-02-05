from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextBrowser
from PySide6.QtCore import QFile, QTextStream
import markdown


class ChangeLog(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("Changelog")

        self.root_dir = parent.root_dir
        self.color_theme = parent.color_theme

        self.setup_ui()
        self.load_changelog()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        self.text_browser = QTextBrowser()
        self.text_browser.setOpenExternalLinks(True)
        self.text_browser.setReadOnly(True)
        
        layout.addWidget(self.text_browser)

    def load_changelog(self):
        changelog_path = self.root_dir / "CHANGELOG.md"
        
        if not changelog_path.exists():
            self.text_browser.setText("CHANGELOG.md file not found.")
            return
        
        try:
            file = QFile(str(changelog_path))
            
            if file.open(QFile.ReadOnly | QFile.Text):
                stream = QTextStream(file)
                markdown_text = stream.readAll()
                file.close()
                
                html_content = markdown.markdown(markdown_text)
                self.text_browser.setHtml(html_content)
            
            else:
                self.text_browser.setText("Cannot open CHANGELOG.md file.")
                
        except Exception as e:
            self.text_browser.setText(f"Error loading changelog: {str(e)}")