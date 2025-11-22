import time
import random
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
    # <div class="MuiAlert-message css-1xsto0d"><div class="MuiTypography-root MuiTypography-body1 MuiTypography-gutterBottom MuiAlertTitle-root css-pp3c2j"><p class="MuiTypography-root MuiTypography-body1 title css-ko3ua3">SUCCESS</p></div>Quiz berhasil dibuat</div>
    i=0
    while True:
        i+=1
        try:
            if i==1:
                try:
                    WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "MuiSnackbar-root"))
                    )
                        # if (popup) popup.remove();
                    driver.execute_script("""
                        let popup = document.querySelector('.MuiSnackbar-root');
                        if (popup && popup.innerText.includes('Quiz berhasil')) {
                            popup.style.display = 'none';
                        }
                    """)
                    print("Pop-up berhasil dihapus.")
                except:
                    print("Pop-up tidak ditemukan atau sudah hilang.")

            pertanyaan_elem = wait.until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".ck-content p"))
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

def quisioner(driver, nama_matkul, pertemuan, ran=False):
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

        pilihan = random.choice(radio_buttons) if ran else radio_buttons[0]

        # Klik langsung
        pilihan.click()

    submit_button= wait.until(
        EC.visibility_of_element_located((By.XPATH, f"//button[contains(text(),'Submit Kuesioner')]"))
    )
    submit_button.click()

    # time.sleep(5)


# name="row-radio-buttons-group"
def pilihan(take_data= True):
    driver= set_driver(headless=True)

    driver.get(link)
    WebDriverWait(driver, timeout=300).until(
        lambda d: "Dashboard" in d.page_source
    )

    matkul= matkul_pert(driver)

    driver.quit()

    return matkul

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


def main():
    matkul= pilihan()
    # pilih_semester(driver) ##ppp

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
            if tipe== 'Kuesioner':
                driver.get(link)
                WebDriverWait(driver, timeout=300).until(
                    lambda d: "Dashboard" in d.page_source
                )
                quisioner(driver, nama_matkul, nama_pert, ran=True)
                
            if tipe == 'Posttest':
                driver.get(link)
                WebDriverWait(driver, timeout=300).until(
                    lambda d: "Dashboard" in d.page_source
                )
                quiz(driver, nama_matkul, nama_pert, tipe)
                driver.get(link)
                WebDriverWait(driver, timeout=300).until(
                    lambda d: "Dashboard" in d.page_source
                )
                quisioner(driver, nama_matkul, nama_pert, ran=True)
                
        finally:
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