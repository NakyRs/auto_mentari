import json
from pathlib import Path

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

    # return data

def writeFileJson(obj, filename):
    file_path = CONFIG_DIR / filename
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)  # buat folder jika belum ada

    jsonObj = json.dumps(obj, indent=4)

    with open(file_path, "w", encoding='utf-8') as outfile:
        outfile.write(jsonObj)

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