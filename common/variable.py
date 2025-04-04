import os
import httpx
import sys
import winreg
import ujson as json
from pathlib import Path


def get_steam_path(config: dict) -> Path:
    """Get Steam installation path"""
    try:
        if custom_path := config.get("Custom_Steam_Path"):
            return Path(custom_path)

        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Valve\Steam") as key:
            return Path(winreg.QueryValueEx(key, "SteamPath")[0])
    except Exception as e:
        print(f"Failed to get Steam path: {str(e)}")
        sys.exit(1)


DEFAULT_CONFIG = {
    "Github_Personal_Token": "",
    "Custom_Steam_Path": "",
    "Debug_Mode": False,
    "Logging_Files": True,
    "Help": "GitHub Personal Token can be generated in Developer settings of GitHub settings",
}


def generate_config() -> None:
    try:
        with open(Path("./config.json"), "w", encoding="utf-8") as f:
            f.write(json.dumps(DEFAULT_CONFIG, indent=2, ensure_ascii=False))
        print("Configuration file generated")
    except IOError as e:
        print(f"Failed to create config file: {str(e)}")
        sys.exit(1)


def load_config() -> dict:
    if not Path("./config.json").exists():
        generate_config()
        print("Please fill in the config file and restart the program")
        os.system("pause")

    try:
        with open(Path("./config.json"), "r", encoding="utf-8") as f:
            return json.loads(f.read())
    except json.JSONDecodeError:
        print("Config file corrupted, regenerating...")
        generate_config()
        sys.exit(1)
    except Exception as e:
        print(f"Failed to load config: {str(e)}")
        sys.exit(1)


CLIENT = httpx.AsyncClient(verify=False)
CONFIG = load_config()
DEBUG_MODE = CONFIG.get("Debug_Mode", False)
LOG_FILE = CONFIG.get("Logging_Files", True)
GITHUB_TOKEN = str(CONFIG.get("Github_Personal_Token", ""))
STEAM_PATH = get_steam_path(CONFIG)
IS_CN = True
HEADER = {"Authorization": f"Bearer {GITHUB_TOKEN}"} if GITHUB_TOKEN else None
REPO_LIST = [
    "SteamAutoCracks/ManifestHub",
    "ikun0014/ManifestHub",
    "Auiowu/ManifestAutoUpdate",
]
