# Traducator Multilingual cu Sistem de Login


## Aplicatie Python care permite traducerea textelor, detectarea limbii, incarcarea si salvarea PDF-urilor, si acces securizat prin sistem de Login/Register.

Module si API-uri folosite:
* Tkinter (interfata grafica)
* deep-translator (Google Translate API)
* langdetect (detectarea limbii)
* bcrypt (criptare parole)
* SQLite3 (baza de date pentru utilizatori)
* PyPDF2 (citire PDF)
* FPDF (generare PDF)
* PyAudio (microfon)
* SpeechRecognition( recunoastere vorbe)
## Modul de instalare:
* 1. Trebuie clonat repositoriul cu comanda:
```git clone https://github.com/caramida91/Translator.git```

* 2. Creeaza un virtual env pe Linux cu:
```python -m venv venv ```
```source venv/bin/activate```
* Iar pe Windows cu:
```py -m venv venv```
```venv/Scripts/activate```
* 3. Instaleaza dependency-urile cu:
```pip install -r requirements.txt```

* Sau pe rand:
```
pip install deep-translator
pip install langdetect
pip install bcrypt
pip install fpdf
pip install PyPDF2
pip install pyaudio
pip install speechrecognition
```
* 4. Pentru a rula aplicatia, se foloseste:
```python app.py```

## Cum se foloseste:
* 1. Creeaza cont sau autentifica-te in fereastra de Login/Register
* 2. Dupa autentificare se deschide traducatorul complet (afisare.py)
* 3. Introdu text, selecteaza limbi, traduce, incarca PDF sau salveaza PDF

### TREBUIE MARITA FEREASTRA PENTRU A SE VEDEA TOATE BUTOANELE.
