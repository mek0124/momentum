from pathlib import Path


class Config:
    def __init__(self) -> None:
        self.curr_dir = Path(__file__).parent

    def get_config_file_path(self) -> Path:
        app_dir = self.curr_dir.parent
        proj_root = app_dir.parent
        return proj_root / "pyproject.toml"
    
    def get_config_data(self) -> str:
        file_path = self.get_config_file_path()

        try:
            with open(file_path, 'r') as settings_file:
                all_settings = settings_file.read()

            return all_settings
        
        except Exception as e:
            print(f"Unknown Exception: Reading Version: {e}")
            return ""

    def get_version(self) -> str:
        all_settings = self.get_config_data()

        for line in all_settings.split("\n"):
            if line.startswith("version"):
                return line.strip().replace("version", "").replace("=", "").replace(" ", "").replace('"', "")
            
        return "0.1.0"

    def get_app_name(self) -> str:
        all_settings = self.get_config_data()

        for line in all_settings.split("\n"):
            if line.startswith("name"):
                app_name = line.strip().replace("name", "").replace("=", "").replace(" ", "").replace('"', "")
                if "-" in app_name:
                    app_first, app_second = app_name.split("-")
                    return f"{app_first.strip().capitalize()} {app_second.capitalize()}"
                else:
                    return app_name.capitalize()
            
        return "Textual App"