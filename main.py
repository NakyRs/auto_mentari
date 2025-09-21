import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service
from git_model import generate

link= "https://mentari.unpam.ac.id"

def set_driver(headless= False):
    chrome_options = Options()
    chrome_options.add_argument(r"user-data-dir=C:\Users\HP\AppData\Local\Google\Chrome\User Data\Profile 1")  # Lokasi direktori profil pengguna
    if headless:
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--window-size=1920,1080")
    # driver = webdriver.Chrome(service=Service("path_to_chromedriver"), options=chrome_options)

    driver = webdriver.Chrome(options=chrome_options)

    return driver

def matkul_pert(driver):
    def matkul_element():
        return WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located((By.XPATH, '//p[@class="MuiTypography-root MuiTypography-body1 css-d7xg8o"]'))
        )

    matkul= {}
    courses= matkul_element()

    for i in range(len(courses)):
        if i == len(courses)-1: continue
        course= matkul_element()
        namat= course[i].text

        course[i].click()
        pertemuan_elements = WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located((By.XPATH, '//h6[@class="MuiTypography-root MuiTypography-h6 css-l5x8uf"]'))
        )
        pertemuan_list = []
        for j, pertemuan in enumerate(pertemuan_elements):
            # print(f"  Pertemuan {j}: {pertemuan.text}")
            if j == 0: continue
            pertemuan_list.append(pertemuan.text)

        matkul[namat]= pertemuan_list

        driver.back()
        WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.XPATH, '//p[@class="MuiTypography-root MuiTypography-body1 css-d7xg8o"]'))
        )

    return matkul


def quiz(driver, nama_matkul, pertemuan, tipe):
    # nama_matkul= nama_matkul.upper() #Test Semester 4       ##ppp

    wait = WebDriverWait(driver, 10)
    element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, f'//div[@role="button" and .//p[text()="{nama_matkul}"]]'))
    )
    element.click()

    pertemuan1 = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, f'//h6[text()="{pertemuan}"]'))
    )
    pertemuan1.click()

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
                EC.presence_of_element_located((By.CSS_SELECTOR, ".ck-content p"))
            )
            pertanyaan = pertanyaan_elem.text.strip()
            # pertanyaan_container = driver.find_element(By.CSS_SELECTOR, "div.MuiPaper-root[id]")
            # pertanyaan_id = pertanyaan_container.get_attribute("id")

            pilihan_labels = driver.find_elements(By.CSS_SELECTOR, "label.MuiFormControlLabel-root")
            opsi_list = []
            for label in pilihan_labels:
                try:
                    huruf = label.find_element(By.CSS_SELECTOR, "p").text.strip()
                    isi = label.find_element(By.CSS_SELECTOR, ".ck-content p").text.strip()
                    opsi_list.append(f"{huruf} {isi}")
                except:
                    continue

            gabungan = pertanyaan + "\n" + "\n".join(opsi_list)
            print(f"\n Soal:\n{gabungan}")

            jawaban = generate(gabungan).strip().upper()
            print(f"Jawaban AI: {jawaban}")

            clicked = False
            for label in pilihan_labels:
                huruf = label.find_element(By.CSS_SELECTOR, "p").text.strip().replace('.', '').upper()
                if huruf == jawaban:
                    label.click()
                    clicked = True
                    print(f"Klik jawaban: {huruf}")
                    break
            if not clicked:
                print("Jawaban tidak ditemukan di pilihan.")
                break

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

def pilihan(take_data= True):
    driver= set_driver(headless=True)

    driver.get(link)
    WebDriverWait(driver, timeout=300).until(
        lambda d: "Dashboard" in d.page_source
    )

    matkul= matkul_pert(driver)

    driver.quit()

    return matkul

def main():
    matkul= pilihan()
    # pilih_semester(driver) ##ppp

    while True:
        list_namat= []
        print("===== Matkul =====")
        for i, mat in enumerate(matkul.keys(), start=1):
            print(f"{i}.", mat)
            list_namat.append(mat)

        no_matkul= int(input("Pilih Matkul: "))
        nama_matkul= list_namat[no_matkul-1]

        list_pert= []
        print("\n===== Pertemuan =====")
        for i, pert in enumerate(matkul[nama_matkul], start=1):
            print(f"{i}.", pert)
            list_pert.append(pert)
        
        no_pert= int(input("Pilih Pertemuan: "))
        nama_pert= list_pert[no_pert-1]

        list_tipe=["Pretest","Posttest"]
        print("==== Type ====")
        for i, tipe in enumerate(list_tipe, start= 1):
            print(f"{i}.", tipe)
        tipe= list_tipe[int(input("Masukkan Tipe: "))-1]

        print(f"=Yang Dipilih=\nMatkul: {nama_matkul}\nPertemuan: {nama_pert}\nTipe: {tipe}")

        if (no_matkul or no_pert) == 0:
            print("=== Bye ===")
            break
        
        driver= set_driver()

        driver.get(link)
        WebDriverWait(driver, timeout=300).until(
            lambda d: "Dashboard" in d.page_source
        )

        quiz(driver, nama_matkul, nama_pert, tipe)
        driver.quit()


if __name__ == "__main__":
    main()




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
    input_element.send_keys(Keys.ARROW_DOWN)
    input_element.send_keys(Keys.ENTER)