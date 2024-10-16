# set -eu

# export PYTHONUNBUFFERED=true

# VIRTUALENV=.data/venv

# if [ ! -d $VIRTUALENV ]; then
#   python3 -m venv $VIRTUALENV
# fi

# if [ ! -f $VIRTUALENV/bin/pip ]; then
#   curl --silent --show-error --retry 5 https://bootstrap.pypa.io/get-pip.py | $VIRTUALENV/bin/python
# fi

# $VIRTUALENV/bin/pip install -r requirements.txt

# $VIRTUALENV/bin/python3 app.py
# Footer
#!/bin/bash

# Hentikan eksekusi script jika ada error (-e) atau variabel yang tidak diinisialisasi (-u)
set -eu

# Non-buffering untuk output Python
export PYTHONUNBUFFERED=true

# Tentukan path untuk virtual environment
VIRTUALENV=.data/venv

# Jika folder virtual environment belum ada, buat virtual environment baru
if [ ! -d $VIRTUALENV ]; then
  python3 -m venv $VIRTUALENV
fi

# Jika pip tidak ada di virtual environment, instal pip
if [ ! -f $VIRTUALENV/bin/pip ]; then
  curl --silent --show-error --retry 5 https://bootstrap.pypa.io/get-pip.py | $VIRTUALENV/bin/python
fi

# Instal semua dependensi yang ada di requirements.txt
$VIRTUALENV/bin/pip install -r requirements.txt

# Jalankan aplikasi Flask
$VIRTUALENV/bin/python3 app.py
