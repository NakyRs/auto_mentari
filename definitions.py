import json

def readFileJson(file):
    print("Membaca File Json...")
    with open(file, 'r') as f:
        return json.loads(f.read())

    # return data

def writeFileJson(obj, file):
    jsonObj = json.dumps(obj, indent=4)

    with open(file, "w") as outfile:
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