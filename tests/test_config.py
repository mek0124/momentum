from config.config import config

def test_app_name():
    assert config.config_data.get("app", {}).get("name") == "Task Manager"

def test_app_version():
    assert config.config_data.get("app", {}).get("version") == "0.6.0"
