from dotenv import load_dotenv

import os


load_dotenv()


class Config:
    storage_version = os.getenv("storage_version", "0.1.0")
    core_version = os.getenv("core_version", "0.1.0")
    cli_version = os.getenv("cli_version", "0.1.0")
    tui_version = os.getenv("tui_version", "0.1.0")
    desktop_version = os.getenv("desktop_version", "0.1.0")
    mobile_version = os.getenv("mobile_version", "0.1.0")
    web_version = os.getenv("web_version", "0.1.0")

    def get_version(self, keyword: str = None) -> dict:
        version_dict = {
            "core_version": self.core_version,
            "cli_version": self.cli_version,
            "tui_version": self.tui_version,
            "desktop_version": self.desktop_version,
            "mobile_version": self.mobile_version,
            "web_version": self.web_version,
        }

        if not keyword.strip():
            return version_dict
        
        return version_dict[keyword]