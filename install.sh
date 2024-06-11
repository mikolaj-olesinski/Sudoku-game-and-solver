#!/bin/bash

# Aktualizacja repozytoriów
sudo apt-get update

# Instalacja python3-venv, jeśli nie jest zainstalowany
sudo apt-get install -y python3-venv

# Tworzenie wirtualnego środowiska
python3 -m venv venv

# Aktywacja wirtualnego środowiska
source venv/bin/activate

# Instalacja pakietów z requirements.txt
pip install -r requirements.txt

echo "Instalacja zakończona. Użyj 'source venv/bin/activate' aby aktywować wirtualne środowisko. Następnie uruchom 'python app.py' aby uruchomić program."
```
