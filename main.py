import time
import random
import os
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.chrome.service import Service
from git_model import generate
from definitions import *

link= "https://mentari.unpam.ac.id"
user_data_path = os.environ['LOCALAPPDATA'] + r'\Google\Chrome\User Data\Profile 1' # Lokasi direktori profil pengguna, Sesuaikan
random_quiz= False
random_quisioner= True

def set_driver(headless= False):
    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument(f"--user-data-dir={user_data_path}")
    if headless:
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
    # driver = webdriver.Chrome(service=Service("path_to_chromedriver"), options=chrome_options)

    driver = uc.Chrome(options=chrome_options, version_main=145) #samakan dengan versi chrome

    return driver

def matkul_pert(driver):
    def matkul_element():
        return WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located((By.XPATH, '//p[@class="MuiTypography-root MuiTypography-body1 css-d7xg8o"]'))
            # EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class,"MuiListItemText-root")]//span//p[contains(@class,"MuiTypography-body1")]'))
        )

    matkul= {}
    courses= matkul_element()

    for i in range(len(courses)):
        if i == len(courses)-1: continue
        course= matkul_element()
        nama_matkul= course[i].text

        course[i].click()
        pertemuan_elements = WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located((By.XPATH, '//h6[@class="MuiTypography-root MuiTypography-h6 css-l5x8uf"]'))
        )
        pertemuan_list = []
        for j, pertemuan in enumerate(pertemuan_elements):
            if j == 0: continue
            pertemuan_list.append(pertemuan.text)

        matkul[nama_matkul]= pertemuan_list

        driver.back()
        WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.XPATH, '//p[@class="MuiTypography-root MuiTypography-body1 css-d7xg8o"]'))
        )

    return matkul


def quiz(driver, nama_matkul, pertemuan, tipe, rand= False):
    # nama_matkul= nama_matkul.upper() #Test Semester 4

    wait = WebDriverWait(driver, 10)
    element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, f'//div[@role="button" and .//p[text()="{nama_matkul}"]]'))
    )
    element.click()

    pertemuan = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, f'//h6[text()="{pertemuan}"]'))
    )
    pertemuan.click()

    # wait.until(
    #     EC.visibility_of_element_located((By.XPATH, f"//p[text()='{pertemuan}' or text()='{pertemuan.capitalize()}']"))
    # )

    # quizzz
    quiz_button = wait.until(
        EC.visibility_of_element_located((By.XPATH, f"//p[text()='{tipe}']/following::button[contains(text(),'Quiz')]"))
    )
    quiz_button.click()

    do_quiz_button= wait.until(
        EC.visibility_of_element_located((By.XPATH, f"//button[contains(text(),'Kerjakan Quiz')]"))
    )
    do_quiz_button.click()

    try:
        start_quiz_button= wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Mulai Quiz')]"))
        )
        start_quiz_button.click()

        confirm_quiz_xpath=(
            "//button[normalize-space()='Ya']"
        )
        confirm_quiz_button= wait.until(
            EC.element_to_be_clickable((By.XPATH, confirm_quiz_xpath))
        )
        confirm_quiz_button.click()
    except:
        pass

    while True:
        try:
            pertanyaan_elem = wait.until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".ck-content p"))
            )
            pertanyaan = pertanyaan_elem.text.strip()
            # pertanyaan_container = driver.find_element(By.CSS_SELECTOR, "div.MuiPaper-root[id]")
            # pertanyaan_id = pertanyaan_container.get_attribute("id")

            pilihan_labels = driver.find_elements(By.CSS_SELECTOR, "label.MuiFormControlLabel-root")
            
            opsi_list= {}
            opsi_text= {}
            for label in pilihan_labels:
                try:
                    huruf = label.find_element(By.CSS_SELECTOR, "p").text.strip().replace('.', '').upper()
                    isi = label.find_element(By.CSS_SELECTOR, ".ck-content p").text.strip()
                    # opsi_list.append(f"{huruf} {isi}")
                    opsi_list[huruf]= label
                    opsi_text[huruf]= isi
                except:
                    continue

            if not rand:
                gabungan = pertanyaan + "\n" + "\n".join(f'{k} {v}' for k, v in opsi_text.items())
                print(f"\n Soal:\n{gabungan}")

                jawaban = generate(gabungan).strip().upper()
                print(f"Jawaban AI: {jawaban}")
            else:
                jawaban= random.choice([k for k in opsi_list.keys()])

            if jawaban in opsi_list.keys():
                opsi_list[jawaban].click()
                print(f'Klik jawaban: {jawaban}')
            else:
                print('jawaban tidak ditemukan')

            try:
                selesai_btn= driver.find_element(By.XPATH, "//button[contains(text(), 'Selesai')]")
                selesai_btn.click()
                
                confirm_quiz_button= wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Ya']"))
                )
                confirm_quiz_button.click()
                print("Kuis selesai. Klik tombol Selesai.")
                break

            except:
                lanjut_btn= driver.find_element(By.XPATH, "//button[contains(text(),'Next')]")
                lanjut_btn.click()
                print("lanjut")

        except Exception as e:
            print("Terjadi error:", e)
            break

def quisioner(driver, nama_matkul, pertemuan, rand=False):
    wait = WebDriverWait(driver, 5)
    element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, f'//div[@role="button" and .//p[text()="{nama_matkul}"]]'))
    )
    element.click()

    pertemuan = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, f'//h6[text()="{pertemuan}"]'))
    )
    pertemuan.click()

    quisioner_button=wait.until(
        EC.visibility_of_element_located((By.XPATH, f"//p[text()='Kuesioner']/following::button[contains(text(),'Kuesioner')]"))
    )
    quisioner_button.click()

    radio_group= wait.until(
        # EC.visibility_of_element_located((By.CSS_SELECTOR, f'MuiFormGroup-root.MuiFormGroup-row.css-p58oka'))
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.MuiFormGroup-root.MuiFormGroup-row"))
    )

    for button in radio_group:
        radio_buttons = button.find_elements(By.CSS_SELECTOR, "input[type='radio']")

        if not radio_buttons:
            print(f"Tidak ditemukan radio")
            continue

        pilihan = random.choice(radio_buttons) if rand else radio_buttons[0]
        pilihan.click()

    try:
        submit_button= wait.until(
            EC.visibility_of_element_located((By.XPATH, f"//button[contains(text(),'Submit Kuesioner')]"))
        )
        submit_button.click()
        print("Sudah Tersubmit")
    except:
        print("Error")
        return False
    # time.sleep(5)

def updateDataMatkul(take_data= True):
    driver= set_driver(headless=True)

    driver.get(link)
    WebDriverWait(driver, timeout=300).until(
        lambda d: "Dashboard" in d.page_source
    )

    matkul= matkul_pert(driver)

    driver.quit()
    writeFileJson(matkul, "matkul.json")
    # return matkul

def main():
    print("=+=+=+=+=+= Auto_E-Learning =+=+=+=+=+=")
    while True:
        pilihan= int(input("1.Update Data\n2.Login\n3.Start\ninput:"))
        if pilihan== 1:
            try:
                updateDataMatkul()
                print("data berhasil diupdate")
            except:
                print('data gagal diupdate')
        elif pilihan== 2:
            login()
        elif pilihan== 3:
            break
        else: "Pilihan Tidak ada"

    try:
        matkul= readFileJson('matkul.json')
    except:
        print("File tidak ditemukan, Membuat File Json...")
        updateDataMatkul()
        matkul= readFileJson('matkul.json')

    while True:
        nama_matkul = pilih_dari_list("Matkul", list(matkul.keys()))
        nama_pert = pilih_dari_list("Pertemuan", matkul[nama_matkul])
        tipe = pilih_dari_list("Tipe", ["Pretest", "Posttest", "Kuesioner"])

        print(f"\n=== Yang Dipilih ===")
        print(f"Matkul: {nama_matkul}")
        print(f"Pertemuan: {nama_pert}")
        print(f"Tipe: {tipe}\n")

        lanjut = input("Lanjut ke proses? (y/n): ").strip().lower()
        if lanjut != 'y':
            print("=== Bye ===")
            break

        driver = set_driver()
        try:
            driver.get(link)
            WebDriverWait(driver, timeout=300).until(
                lambda d: "Dashboard" in d.page_source
            )
            # pilih_semester(driver) ##Test only
            if tipe== 'Kuesioner':
                quisioner(driver, nama_matkul, nama_pert, rand= random_quisioner)
            elif tipe == 'Posttest':
                quiz(driver, nama_matkul, nama_pert, tipe, rand= random_quiz)

                driver.get(link)
                WebDriverWait(driver, timeout=300).until(
                    lambda d: "Dashboard" in d.page_source
                )
                quisioner(driver, nama_matkul, nama_pert, rand= random_quisioner)
            else:
                quiz(driver, nama_matkul, nama_pert, tipe, rand= random_quiz)
                
        finally:
            driver.quit()

def login():
    driver = set_driver()
    driver.get(link)
    print('Login berhasil disimpan')


##Test only
def pilih_semester(driver):
    from selenium.common.exceptions import StaleElementReferenceException
    from selenium.webdriver.common.keys import Keys

    input_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[role='combobox']"))
    )
    try:
        input_element.click()
    except StaleElementReferenceException:
        input_element = driver.find_element(By.CSS_SELECTOR, "input[role='combobox']")
        input_element.click()

    input_element.send_keys(Keys.ARROW_DOWN)
    input_element.send_keys(Keys.ARROW_DOWN)
    input_element.send_keys(Keys.ENTER)


if __name__ == "__main__":
    main()