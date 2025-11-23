import tkinter as tk
from tkinter import ttk
from deep_translator import GoogleTranslator
from langdetect import detect, DetectorFactory

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


def detect_language(text):
    """Detectează limba textului folosind langdetect"""
    try:
        if len(text.strip()) < 3:
            return None
        detected_code = detect(text)
        # Convertește codurile speciale
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
    """Ajustează înălțimea ambelor câmpuri de text (input și rezultat) sincronizat, între 1 și 10 linii"""
    # Obține numărul de linii din fiecare widget
    input_lines = text_input.get("1.0", "end-1c").count('\n') + 1
    result_lines = result_text.get("1.0", "end-1c").count('\n') + 1
    lines = max(input_lines, result_lines)
    lines = min(max(lines, 1), 10)  # clamp între 1 și 10
    text_input.config(height=lines)
    result_text.config(height=lines)
    # Force UI update
    text_input.update_idletasks()
    result_text.update_idletasks()


def translate_text(event=None):
    text = text_input.get("1.0", "end-1c").strip()
    if not text:
        # enable to update, then disable again
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
            result_text.delete("1.0", tk.END)
            result_text.insert("1.0", "⚠️ Limbile sursă și destinație sunt identice.")
            adjust_heights()
            return

        translation = GoogleTranslator(source=source_lang, target=target_lang).translate(text)
        result_text.config(state="normal")
        result_text.delete("1.0", tk.END)
        result_text.insert("1.0", translation)
        result_text.config(state="disabled")
        adjust_heights()

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

    text_input.delete("1.0", tk.END)
    result_text.config(state="normal")
    result_text.delete("1.0", tk.END)
    result_text.config(state="disabled")
    detected_label.config(text="")
    adjust_heights()



root = tk.Tk()
root.title("Traducător Multilingual")
root.geometry("700x500")
root.resizable(True, True)
root.configure(bg="#f5f6fa")


style = ttk.Style()
style.theme_use('clam')
style.configure('Modern.TFrame', background="#f5f6fa")
style.configure('Card.TFrame', background="white", relief="flat")
style.configure('Modern.TLabel', background="#f5f6fa", font=("Segoe UI", 10))
style.configure('Title.TLabel', background="#f5f6fa", font=("Segoe UI", 18, "bold"), foreground="#2c3e50")
style.configure('Modern.TButton', font=("Segoe UI", 10), padding=10)
style.configure('Accent.TButton', font=("Segoe UI", 11, "bold"), padding=12)

main_container = ttk.Frame(root, style='Modern.TFrame')
main_container.pack(fill="both", expand=True, padx=20, pady=20)


title_label = ttk.Label(main_container, text="🌐 Traducător Multilingual", style='Title.TLabel')
title_label.pack(pady=(0, 20))

lang_card = ttk.Frame(main_container, style='Card.TFrame', relief="solid", borderwidth=1)
lang_card.pack(fill="x", pady=(0, 15), ipady=15, ipadx=15)

lang_frame = ttk.Frame(lang_card, style='Card.TFrame')
lang_frame.pack(fill="x", padx=10, pady=5)

source_frame = ttk.Frame(lang_frame, style='Card.TFrame')
source_frame.pack(side="left", expand=True, fill="x", padx=5)

ttk.Label(source_frame, text="Din:", font=("Segoe UI", 10, "bold"), background="white").pack(anchor="w", pady=(0, 5))
source_var = tk.StringVar(value='Detectare Automată')
# Crează lista cu "Detectare Automată" pe primul loc
source_languages = ['Detectare Automată'] + sorted([k for k in LANGUAGES.keys() if k != 'Detectare Automată'])
source_combo = ttk.Combobox(source_frame, textvariable=source_var,
                            values=source_languages,
                            state="readonly", width=25, font=("Segoe UI", 10))
source_combo.pack(fill="x")

swap_button = ttk.Button(lang_frame, text="⇄", command=swap_languages, width=3)
swap_button.pack(side="left", padx=10, pady=15)

target_frame = ttk.Frame(lang_frame, style='Card.TFrame')
target_frame.pack(side="left", expand=True, fill="x", padx=5)

ttk.Label(target_frame, text="În:", font=("Segoe UI", 10, "bold"), background="white").pack(anchor="w", pady=(0, 5))
target_var = tk.StringVar(value='Engleză')
target_combo = ttk.Combobox(target_frame, textvariable=target_var,
                            values=sorted([k for k in LANGUAGES.keys() if k != 'Detectare Automată']),
                            state="readonly", width=25, font=("Segoe UI", 10))
target_combo.pack(fill="x")

detected_label = ttk.Label(main_container, text="", font=("Segoe UI", 9),
                           foreground="#3498db", background="#f5f6fa")
detected_label.pack(pady=(0, 10))

side_by_side = ttk.Frame(main_container, style='Modern.TFrame')
side_by_side.pack(fill="both", expand=True, pady=(0, 10))

side_by_side.columnconfigure(0, weight=1)
side_by_side.columnconfigure(1, weight=1)
side_by_side.rowconfigure(0, weight=1)

input_card = ttk.Frame(side_by_side, style='Card.TFrame', relief="solid", borderwidth=1)
input_card.grid(row=0, column=0, sticky="nsew", padx=(0, 7), pady=0)

ttk.Label(input_card, text="📝 Text de tradus:", font=("Segoe UI", 10, "bold"),
          background="white").pack(anchor="w", padx=15, pady=(10, 5))

text_input = tk.Text(input_card, height=1, font=("Segoe UI", 11), wrap=tk.WORD,
                     relief="flat", bg="white", fg="#2c3e50", insertbackground="#3498db",
                     padx=10, pady=10)
text_input.pack(fill="both", expand=True, padx=15, pady=(0, 10))
text_input.bind("<KeyRelease>", adjust_heights)
text_input.focus()

result_card = ttk.Frame(side_by_side, style='Card.TFrame', relief="solid", borderwidth=1)
result_card.grid(row=0, column=1, sticky="nsew", padx=(7, 0), pady=0)

ttk.Label(result_card, text="✨ Rezultat:", font=("Segoe UI", 10, "bold"),
          background="white").pack(anchor="w", padx=15, pady=(10, 5))

result_text = tk.Text(result_card, height=1, font=("Segoe UI", 11), wrap=tk.WORD,
                      relief="flat", bg="#f8f9fa", fg="#2c3e50",
                      padx=10, pady=10, state="disabled")
result_text.pack(fill="both", expand=True, padx=15, pady=(0, 10))

button_frame = ttk.Frame(main_container, style='Modern.TFrame')
button_frame.pack(pady=10)

clear_button = ttk.Button(button_frame, text="🗑️ Șterge", command=clear_all, style='Modern.TButton')
clear_button.pack(side="left", padx=5)

translate_button = ttk.Button(button_frame, text="🔄 Tradu", command=translate_text, style='Accent.TButton')
translate_button.pack(side="left", padx=5)

text_input.bind("<Control-Return>", translate_text)

adjust_heights()

root.mainloop()