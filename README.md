# Auto_Mentari

Otomatiasi E-learning mentari unpam menggunakan selenium dengan AI dari [github model](https://github.com/marketplace/models)
## Installation
Clone atau download [Repo](https://github.com/NakyRs/auto_mentari) ini
```bash
git clone https://github.com/NakyRs/auto_mentari.git
```

Gunakan package manager [pip](https://pip.pypa.io/en/stable/) to install.

```bash
pip install -r requirements.txt
```

## Usage
set token di git_model.py
```python
token = "YOUR_GITHUB_TOKEN" # <--Model Token
```
```bash
python main.py
```
1. login (Manual)
2. Update Data (Menyimpan data matkul)
3. Start 
### Random Option
```python
random_quiz= False # ubah ke True pada kode jika ingin jawaban random tanpa github model
random_quisioner= True
```