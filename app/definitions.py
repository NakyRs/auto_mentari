import json
from pathlib import Path
import re
import subprocess
import platform
import os

# Folder app sebagai base
APP_DIR = Path(__file__).resolve().parent
CONFIG_DIR = APP_DIR / "config"

def readFileJson(filename):
    file_path = CONFIG_DIR / filename
    if not file_path.exists():
        raise FileNotFoundError(f"File {filename} tidak ditemukan di {CONFIG_DIR}")
    
    print(f"Membaca File Json...{filename}")
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def writeFileJson(obj, filename):
    file_path = CONFIG_DIR / filename
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)  # buat folder jika belum ada

    jsonObj = json.dumps(obj, indent=4)

    with open(file_path, "w", encoding='utf-8') as outfile:
        outfile.write(jsonObj)

def get_chrome_user_data_path(profile="Default"):
    system = platform.system()

    if system == "Windows":
        base_path = os.path.join(
            os.environ.get("LOCALAPPDATA", ""),
            "Google", "Chrome", "User Data"
        )
    elif system == "Darwin":
        base_path = os.path.expanduser(
            "~/Library/Application Support/Google/Chrome"
        )
    elif system == "Linux":
        base_path = os.path.expanduser(
            "~/.config/google-chrome"
        )
    else:
        raise Exception("OS tidak dikenali")
    
    return os.path.join(base_path, profile)
    
def get_chrome_version():
    system = platform.system()

    if system == "Windows":
        return get_chrome_version_windows()
    elif system == "Darwin":
        return get_chrome_version_mac()
    elif system == "Linux":
        return get_chrome_version_linux()
    else:
        print("OS tidak dikenali")
        return None
    
def get_chrome_version_windows():
    try:
        output = subprocess.check_output(
            r'reg query "HKEY_CURRENT_USER\Software\Google\Chrome\BLBeacon" /v version',
            shell=True
        ).decode()
        version = re.search(r"(\d+)\.", output).group(1)
        return int(version)
    except:
        return None
    
def get_chrome_version_mac():
    try:
        output = subprocess.check_output(
            ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "--version"]
        ).decode()

        version = re.search(r"(\d+)\.", output).group(1)
        return int(version)
    except Exception as e:
        print("Gagal ambil versi Chrome (macOS):", e)
        return None

def get_chrome_version_linux():
    commands = [
        "google-chrome",
        "google-chrome-stable",
        "chromium-browser",
        "chromium"
    ]

    for cmd in commands:
        try:
            output = subprocess.check_output(
                [cmd, "--version"],
                stderr=subprocess.DEVNULL
            ).decode()

            version = re.search(r"(\d+)\.", output).group(1)
            return int(version)
        except:
            continue

    print("Chrome tidak ditemukan di Linux")
    return None

def pilih_dari_list(prompt, daftar):
    while True:
        print(f"\n===== {prompt} =====")
        for i, item in enumerate(daftar, start=1):
            print(f"{i}. {item}")
        try:
            pilihan = int(input(f"Pilih {prompt}: "))
            if 1 <= pilihan <= len(daftar):
                return daftar[pilihan - 1]
            else:
                print("Pilihan di luar jangkauan. Coba lagi.")
        except ValueError:
            print("Masukkan angka yang valid.")