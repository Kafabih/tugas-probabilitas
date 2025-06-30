# 📘 Panduan Instalasi dan Menjalankan Project

Panduan langkah demi langkah untuk:
- Install Python menggunakan **pyenv**
- Membuat virtual environment (**venv**)
- Menjalankan project

---

## 🟢 1. Persiapan (macOS dan Windows)

Pastikan sudah terinstall:
- Git
- Build tools

**MAC OS:**
# Install Homebrew (jika belum)
bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install dependencies
brew install openssl readline sqlite3 xz zlib tcl-tk
Windows:

Install Git for Windows

Install Visual Studio Build Tools

🟢 2. Install pyenv
macOS:
brew install pyenv

Tambahkan ke shell profile (.zshrc atau .bashrc):
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init --path)"' >> ~/.zshrc
source ~/.zshrc

Windows:
Install pyenv-win:
git clone https://github.com/pyenv-win/pyenv-win.git $HOME\.pyenv
setx PATH "$HOME\.pyenv\pyenv-win\bin;$HOME\.pyenv\pyenv-win\shims;%PATH%"

🟢 3. Install Python versi tertentu
Misal Python 3.10.11:

pyenv install 3.10.11

pyenv global 3.10.11

Verifikasi versi:
python --version

🟢 4. Membuat Virtual Environment
Pindah ke folder project:
cd path/to/your/project

Buat virtual environment:
python -m venv venv

🟢 5. Aktivasi Virtual Environment
macOS / Linux:
source venv/bin/activate

Windows (PowerShell):
.\venv\Scripts\Activate

🟢 6. Install Dependensi Project
Pastikan virtual environment aktif, lalu:


pip install -r requirements.txt
🟢 7. Menjalankan Project
Contoh menjalankan script Python utama:
python main.py

Atau jika menggunakan Jupyter Notebook:
jupyter notebook

🟢 8. Deaktivasi Virtual Environment
Jika sudah selesai:
deactivate

🟢 9. Tips Tambahan
✅ Jika pyenv tidak terdeteksi, restart terminal setelah menambahkan PATH.
✅ Untuk update pyenv:

macOS:
brew upgrade pyenv

Windows:
cd $HOME\.pyenv\pyenv-win
git pull
✅ Jika ingin menghapus virtual environment, cukup hapus folder venv.

