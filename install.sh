#!/bin/bash

# Aktualizacja repozytoriów
sudo apt-get update

# Instalacja python3, jeśli nie jest zainstalowany
sudo apt-get install -y python3-venv python3-dev

# Instalacja pakietów
sudo apt-get install -y pkg-config build-essential libdouble-conversion-dev libhdf5-dev

# Tworzenie wirtualnego środowiska
python3 -m venv venv

# Aktywacja wirtualnego środowiska
source venv/bin/activate

# Instalacja setuptools
pip install h5py
pip install setuptools

# Instalacja pakietów z requirements.txt, jeśli istnieje
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
fi

# Instalacja projektu za pomocą setuptools
pip install .

echo "Instalacja zakończona. Użyj 'source venv/bin/activate' aby aktywować wirtualne środowisko. Następnie uruchom 'python app.py' aby uruchomić program."
