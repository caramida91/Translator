### Traducator Multilingual cu Sistem de Login

Scopul proiectului:
Aplicatie Python care permite traducerea textelor, detectarea limbii, incarcarea si salvarea PDF-urilor, si acces securizat prin sistem de Login/Register.

Module si API-uri folosite:
- Tkinter (interfata grafica)
- deep-translator (Google Translate API)
- langdetect (detectarea limbii)
- bcrypt (criptare parole)
- SQLite3 (baza de date pentru utilizatori)
- PyPDF2 (citire PDF)
- FPDF (generare PDF)

Instalare dependente necesare:
pip install deep-translator
pip install langdetect
pip install bcrypt
pip install fpdf
pip install PyPDF2

Sau toate odata:
pip install deep-translator langdetect bcrypt fpdf PyPDF2

Cum se foloseste:
1. Ruleaza fisierul app.py
2. Creeaza cont sau autentifica-te in fereastra de Login/Register
3. Dupa autentificare se deschide traducatorul complet (afisare.py)
4. Introdu text, selecteaza limbi, traduce, incarca PDF sau salveaza PDF
