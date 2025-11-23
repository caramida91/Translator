import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from deep_translator import GoogleTranslator
from langdetect import detect, DetectorFactory
import PyPDF2
from fpdf import FPDF
import os

# Setează seed pentru rezultate consistente
DetectorFactory.seed = 0

# Lista completă de limbi suportate de Google Translate
LANGUAGES = {
    'Detectare Automată': 'auto',
    'Afrikaans': 'af',
    'Albaneză': 'sq',
    'Amharică': 'am',
    'Arabă': 'ar',
    'Armeană': 'hy',
    'Azerbaijană': 'az',
    'Bască': 'eu',
    'Belarusă': 'be',
    'Bengaleză': 'bn',
    'Bosniacă': 'bs',
    'Bulgară': 'bg',
    'Catalană': 'ca',
    'Cebuană': 'ceb',
    'Cehă': 'cs',
    'Chichewa': 'ny',
    'Chineză (Simplificată)': 'zh-CN',
    'Chineză (Tradițională)': 'zh-TW',
    'Coreeană': 'ko',
    'Corsicană': 'co',
    'Croată': 'hr',
    'Daneză': 'da',
    'Engleză': 'en',
    'Esperanto': 'eo',
    'Estonă': 'et',
    'Filipineză': 'tl',
    'Finlandeză': 'fi',
    'Franceză': 'fr',
    'Friziană': 'fy',
    'Galiciană': 'gl',
    'Georgiană': 'ka',
    'Germană': 'de',
    'Greacă': 'el',
    'Gujarati': 'gu',
    'Haitiană': 'ht',
    'Hausa': 'ha',
    'Hawaiană': 'haw',
    'Hindi': 'hi',
    'Hmong': 'hmn',
    'Igbo': 'ig',
    'Indoneziană': 'id',
    'Irlandeză': 'ga',
    'Islandeză': 'is',
    'Italiană': 'it',
    'Japoneză': 'ja',
    'Javaneză': 'jw',
    'Kannada': 'kn',
    'Kazahă': 'kk',
    'Khmeră': 'km',
    'Kurdă': 'ku',
    'Kârgâză': 'ky',
    'Laoțiană': 'lo',
    'Latină': 'la',
    'Letonă': 'lv',
    'Lituaniană': 'lt',
    'Luxemburgheză': 'lb',
    'Macedoneană': 'mk',
    'Maghiară': 'hu',
    'Malgașă': 'mg',
    'Malaeză': 'ms',
    'Malayalam': 'ml',
    'Malteză': 'mt',
    'Maori': 'mi',
    'Marathi': 'mr',
    'Mongolă': 'mn',
    'Birmană': 'my',
    'Nepaleză': 'ne',
    'Norvegiană': 'no',
    'Olandeză': 'nl',
    'Pashto': 'ps',
    'Persană': 'fa',
    'Poloneză': 'pl',
    'Portugheză': 'pt',
    'Punjabi': 'pa',
    'Română': 'ro',
    'Rusă': 'ru',
    'Samoană': 'sm',
    'Sârbă': 'sr',
    'Sesotho': 'st',
    'Shona': 'sn',
    'Sindhi': 'sd',
    'Singaleză': 'si',
    'Slovacă': 'sk',
    'Slovenă': 'sl',
    'Somaleză': 'so',
    'Spaniolă': 'es',
    'Suedeză': 'sv',
    'Sundaneză': 'su',
    'Swahili': 'sw',
    'Tadjikă': 'tg',
    'Tamil': 'ta',
    'Telugu': 'te',
    'Thailandeză': 'th',
    'Turcă': 'tr',
    'Ucraineană': 'uk',
    'Urdu': 'ur',
    'Uzbekă': 'uz',
    'Velșă': 'cy',
    'Vietnameză': 'vi',
    'Xhosa': 'xh',
    'Idiș': 'yi',
    'Yoruba': 'yo',
    'Zulu': 'zu',
    'Ebraică': 'iw',
    'Gaelică Scoțiană': 'gd'
}

# Dicționar invers pentru conversie cod -> nume
CODE_TO_NAME = {v: k for k, v in LANGUAGES.items()}

# Variabilă globală pentru calea PDF-ului încărcat
current_pdf_path = None


def detect_language(text):
    """Detectează limba textului folosind langdetect"""
    try:
        if len(text.strip()) < 3:
            return None
        detected_code = detect(text)
        if detected_code == 'zh-cn':
            detected_code = 'zh-CN'
        elif detected_code == 'zh-tw':
            detected_code = 'zh-TW'
        elif detected_code == 'he':
            detected_code = 'iw'
        return detected_code
    except:
        return None


def adjust_heights(event=None):
    """Funcție păstrată pentru compatibilitate, dar nu mai ajustează înălțimea"""
    pass


def extract_text_from_pdf(pdf_path):
    """Extrage textul din PDF"""
    try:
        text = ""
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        messagebox.showerror("Eroare PDF", f"Nu s-a putut citi PDF-ul:\n{str(e)}")
        return None


def load_pdf():
    """Încarcă un PDF și extrage textul"""
    global current_pdf_path
    file_path = filedialog.askopenfilename(
        title="Selectează un fișier PDF",
        filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
    )

    if file_path:
        current_pdf_path = file_path
        text = extract_text_from_pdf(file_path)

        if text:
            text_input.delete("1.0", tk.END)
            text_input.insert("1.0", text)
            pdf_status_label.config(text=f"📄 Încărcat: {os.path.basename(file_path)}")
            adjust_heights()
            # Activează butonul de download
            download_button.config(state="normal")
        else:
            pdf_status_label.config(text="❌ Eroare la încărcarea PDF-ului")


def create_pdf(text, output_path):
    """Creează un PDF cu textul tradus"""
    try:
        pdf = FPDF()
        pdf.add_page()

        # Adaugă font care suportă UTF-8
        pdf.add_font('DejaVu', '', 'DejaVuSans.ttf', uni=True)
        pdf.set_font('DejaVu', '', 12)

        # Încearcă să folosească DejaVu, dacă nu merge folosește Arial
        try:
            pdf.set_font('DejaVu', '', 12)
        except:
            pdf.set_font('Arial', '', 12)

        # Adaugă text cu word wrap
        pdf.multi_cell(0, 10, text)
        pdf.output(output_path)
        return True
    except Exception as e:
        # Dacă nu merge cu fontul personalizat, încearcă cu metoda simplă
        try:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font('Arial', '', 12)
            # Encodează textul pentru a evita probleme
            safe_text = text.encode('latin-1', 'replace').decode('latin-1')
            pdf.multi_cell(0, 10, safe_text)
            pdf.output(output_path)
            return True
        except Exception as e2:
            messagebox.showerror("Eroare PDF", f"Nu s-a putut crea PDF-ul:\n{str(e2)}")
            return False


def download_pdf():
    """Salvează traducerea ca PDF"""
    result = result_text.get("1.0", "end-1c").strip()

    if not result or result.startswith("⚠️") or result.startswith("❌"):
        messagebox.showwarning("Atenție", "Nu există text tradus de salvat!")
        return

    file_path = filedialog.asksaveasfilename(
        title="Salvează PDF-ul tradus",
        defaultextension=".pdf",
        filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
    )

    if file_path:
        if create_pdf(result, file_path):
            messagebox.showinfo("Succes", f"PDF salvat cu succes:\n{os.path.basename(file_path)}")
            pdf_status_label.config(text=f"💾 Salvat: {os.path.basename(file_path)}")


def translate_text(event=None):
    text = text_input.get("1.0", "end-1c").strip()
    if not text:
        result_text.config(state="normal")
        result_text.delete("1.0", tk.END)
        result_text.insert("1.0", "⚠️ Scrie ceva mai întâi.")
        result_text.config(state="disabled")
        adjust_heights()
        return

    try:
        source_name = source_var.get()
        source_lang = LANGUAGES[source_name]

        if source_lang == 'auto':
            detected_code = detect_language(text)
            if detected_code:
                detected_name = CODE_TO_NAME.get(detected_code, detected_code.upper())
                detected_label.config(text=f"📍 Limbă detectată: {detected_name}")
                source_lang = detected_code
            else:
                detected_label.config(text="⚠️ Nu s-a putut detecta limba")
                return
        else:
            detected_label.config(text="")

        target_name = target_var.get()
        target_lang = LANGUAGES[target_name]

        if source_lang == target_lang:
            result_text.config(state="normal")
            result_text.delete("1.0", tk.END)
            result_text.insert("1.0", "⚠️ Limbile sursă și destinație sunt identice.")
            result_text.config(state="disabled")
            adjust_heights()
            return

        translation = GoogleTranslator(source=source_lang, target=target_lang).translate(text)
        result_text.config(state="normal")
        result_text.delete("1.0", tk.END)
        result_text.insert("1.0", translation)
        result_text.config(state="disabled")
        adjust_heights()

        # Activează butonul de download după traducere
        download_button.config(state="normal")

    except Exception as e:
        result_text.config(state="normal")
        result_text.delete("1.0", tk.END)
        result_text.insert("1.0", f"❌ Eroare: {str(e)}")
        result_text.config(state="disabled")
        adjust_heights()


def swap_languages():
    source = source_var.get()
    target = target_var.get()

    if source != 'Detectare Automată':
        source_var.set(target)
        target_var.set(source)


def clear_all():
    global current_pdf_path
    current_pdf_path = None
    text_input.delete("1.0", tk.END)
    result_text.config(state="normal")
    result_text.delete("1.0", tk.END)
    result_text.config(state="disabled")
    detected_label.config(text="")
    pdf_status_label.config(text="")
    download_button.config(state="disabled")
    adjust_heights()


# Creare fereastră principală
root = tk.Tk()
root.title("Traducător Multilingual")
root.geometry("700x500")
root.resizable(True, True)
root.configure(bg="#f5f6fa")

# Stiluri
style = ttk.Style()
style.theme_use('clam')
style.configure('Modern.TFrame', background="#f5f6fa")
style.configure('Card.TFrame', background="white", relief="flat")
style.configure('Modern.TLabel', background="#f5f6fa", font=("Segoe UI", 10))
style.configure('Title.TLabel', background="#f5f6fa", font=("Segoe UI", 18, "bold"), foreground="#2c3e50")
style.configure('Modern.TButton', font=("Segoe UI", 10), padding=10)
style.configure('Accent.TButton', font=("Segoe UI", 11, "bold"), padding=12)

# Container principal
main_container = ttk.Frame(root, style='Modern.TFrame')
main_container.pack(fill="both", expand=True, padx=20, pady=20)

# Titlu
title_label = ttk.Label(main_container, text="🌐 Traducător Multilingual", style='Title.TLabel')
title_label.pack(pady=(0, 20))

# Card pentru selecție limbi
lang_card = ttk.Frame(main_container, style='Card.TFrame', relief="solid", borderwidth=1)
lang_card.pack(fill="x", pady=(0, 15), ipady=15, ipadx=15)

lang_frame = ttk.Frame(lang_card, style='Card.TFrame')
lang_frame.pack(fill="x", padx=10, pady=5)

# Limbă sursă
source_frame = ttk.Frame(lang_frame, style='Card.TFrame')
source_frame.pack(side="left", expand=True, fill="x", padx=5)

ttk.Label(source_frame, text="Din:", font=("Segoe UI", 10, "bold"), background="white").pack(anchor="w", pady=(0, 5))
source_var = tk.StringVar(value='Detectare Automată')
source_languages = ['Detectare Automată'] + sorted([k for k in LANGUAGES.keys() if k != 'Detectare Automată'])
source_combo = ttk.Combobox(source_frame, textvariable=source_var,
                            values=source_languages,
                            state="readonly", width=25, font=("Segoe UI", 10))
source_combo.pack(fill="x")

# Buton swap
swap_button = ttk.Button(lang_frame, text="⇄", command=swap_languages, width=3)
swap_button.pack(side="left", padx=10, pady=15)

# Limbă destinație
target_frame = ttk.Frame(lang_frame, style='Card.TFrame')
target_frame.pack(side="left", expand=True, fill="x", padx=5)

ttk.Label(target_frame, text="În:", font=("Segoe UI", 10, "bold"), background="white").pack(anchor="w", pady=(0, 5))
target_var = tk.StringVar(value='Engleză')
target_combo = ttk.Combobox(target_frame, textvariable=target_var,
                            values=sorted([k for k in LANGUAGES.keys() if k != 'Detectare Automată']),
                            state="readonly", width=25, font=("Segoe UI", 10))
target_combo.pack(fill="x")

# Label pentru limba detectată
detected_label = ttk.Label(main_container, text="", font=("Segoe UI", 9),
                           foreground="#3498db", background="#f5f6fa")
detected_label.pack(pady=(0, 5))

# Label pentru status PDF
pdf_status_label = ttk.Label(main_container, text="", font=("Segoe UI", 9),
                             foreground="#27ae60", background="#f5f6fa")
pdf_status_label.pack(pady=(0, 10))

# Side by side pentru text
side_by_side = ttk.Frame(main_container, style='Modern.TFrame')
side_by_side.pack(fill="both", expand=True, pady=(0, 10))

side_by_side.columnconfigure(0, weight=1)
side_by_side.columnconfigure(1, weight=1)
side_by_side.rowconfigure(0, weight=1)

# Card input
input_card = ttk.Frame(side_by_side, style='Card.TFrame', relief="solid", borderwidth=1)
input_card.grid(row=0, column=0, sticky="nsew", padx=(0, 7), pady=0)

ttk.Label(input_card, text="📝 Text de tradus:", font=("Segoe UI", 10, "bold"),
          background="white").pack(anchor="w", padx=15, pady=(10, 5))

# Frame pentru text input cu scrollbar
input_text_frame = ttk.Frame(input_card, style='Card.TFrame')
input_text_frame.pack(fill="both", expand=True, padx=15, pady=(0, 10))

input_scrollbar = ttk.Scrollbar(input_text_frame)
input_scrollbar.pack(side="right", fill="y")

text_input = tk.Text(input_text_frame, height=10, font=("Segoe UI", 11), wrap=tk.WORD,
                     relief="flat", bg="white", fg="#2c3e50", insertbackground="#3498db",
                     padx=10, pady=10, yscrollcommand=input_scrollbar.set)
text_input.pack(side="left", fill="both", expand=True)

input_scrollbar.config(command=text_input.yview)
text_input.focus()

# Card rezultat
result_card = ttk.Frame(side_by_side, style='Card.TFrame', relief="solid", borderwidth=1)
result_card.grid(row=0, column=1, sticky="nsew", padx=(7, 0), pady=0)

ttk.Label(result_card, text="✨ Rezultat:", font=("Segoe UI", 10, "bold"),
          background="white").pack(anchor="w", padx=15, pady=(10, 5))

# Frame pentru result text cu scrollbar
result_text_frame = ttk.Frame(result_card, style='Card.TFrame')
result_text_frame.pack(fill="both", expand=True, padx=15, pady=(0, 10))

result_scrollbar = ttk.Scrollbar(result_text_frame)
result_scrollbar.pack(side="right", fill="y")

result_text = tk.Text(result_text_frame, height=10, font=("Segoe UI", 11), wrap=tk.WORD,
                      relief="flat", bg="#f8f9fa", fg="#2c3e50",
                      padx=10, pady=10, state="disabled", yscrollcommand=result_scrollbar.set)
result_text.pack(side="left", fill="both", expand=True)

result_scrollbar.config(command=result_text.yview)

# Frame pentru butoane
button_frame = ttk.Frame(main_container, style='Modern.TFrame')
button_frame.pack(pady=10)

# Butoane cu design modern
pdf_button = tk.Button(button_frame, text="📄 Încarcă PDF", command=load_pdf,
                       font=("Segoe UI", 11, "bold"), bg="#00d2d3", fg="white",
                       relief="flat", padx=20, pady=12, cursor="hand2",
                       activebackground="#00a8a9")
pdf_button.pack(side="left", padx=5)

clear_button = tk.Button(button_frame, text="🗑️ Șterge", command=clear_all,
                         font=("Segoe UI", 11, "bold"), bg="#ff6b6b", fg="white",
                         relief="flat", padx=20, pady=12, cursor="hand2",
                         activebackground="#ee5a52")
clear_button.pack(side="left", padx=5)

translate_button = tk.Button(button_frame, text="🔄 Tradu", command=translate_text,
                             font=("Segoe UI", 11, "bold"), bg="#5f27cd", fg="white",
                             relief="flat", padx=20, pady=12, cursor="hand2",
                             activebackground="#341f97")
translate_button.pack(side="left", padx=5)

download_button = tk.Button(button_frame, text="💾 Descarcă PDF", command=download_pdf,
                            font=("Segoe UI", 11, "bold"), bg="#00d2d3", fg="white",
                            relief="flat", padx=20, pady=12, cursor="hand2",
                            activebackground="#00a8a9", state="disabled")
download_button.pack(side="left", padx=5)

# Bind Ctrl+Enter pentru traducere rapidă
text_input.bind("<Control-Return>", translate_text)

adjust_heights()

root.mainloop()