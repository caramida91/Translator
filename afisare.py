import tkinter as tk
from tkinter import ttk
from deep_translator import GoogleTranslator

# configurare direcție inițială
current_direction = ("ro", "en")  # (sursa, destinația)

def translate_text():
    text = text_input.get()
    if not text.strip():
        result_var.set("⚠️ Scrie ceva mai întâi.")
        return
    try:
        translation = GoogleTranslator(source=current_direction[0], target=current_direction[1]).translate(text)
        result_var.set(translation)
    except Exception as e:
        result_var.set(f"Eroare: {e}")

def switch_direction():
    global current_direction
    # inversează direcția (ro->en <-> en->ro)
    if current_direction == ("ro", "en"):
        current_direction = ("en", "ro")
        direction_var.set("Engleză → Română")
    else:
        current_direction = ("ro", "en")
        direction_var.set("Română → Engleză")
    # șterge textul și rezultatul la schimbare
    text_input.delete(0, tk.END)
    result_var.set("")

# Fereastra principală
root = tk.Tk()
root.title("Traducător Română ↔ Engleză")
root.geometry("440x300")
root.resizable(False, False)

# Titlu
title_label = ttk.Label(root, text="Traducător Română ↔ Engleză", font=("Segoe UI", 14, "bold"))
title_label.pack(pady=10)

# Direcție curentă
direction_var = tk.StringVar(value="Română → Engleză")
direction_label = ttk.Label(root, textvariable=direction_var, font=("Segoe UI", 11))
direction_label.pack()

# Buton pentru schimbare direcție
switch_button = ttk.Button(root, text="🔄 Schimbă direcția", command=switch_direction)
switch_button.pack(pady=5)

# Câmp text
ttk.Label(root, text="Text de tradus:").pack()
text_input = ttk.Entry(root, width=55)
text_input.pack(pady=6)
text_input.focus()

# Buton de traducere
translate_button = ttk.Button(root, text="Tradu", command=translate_text)
translate_button.pack(pady=10)

# Rezultat
ttk.Label(root, text="Rezultat:").pack()
result_var = tk.StringVar()
result_label = ttk.Label(root, textvariable=result_var, font=("Segoe UI", 12, "bold"), wraplength=400)
result_label.pack(pady=8)

# Rulează aplicația
root.mainloop()