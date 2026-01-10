import tkinter as tk
from DataBase.database import DatabaseManager
from Interface.login_window import LoginWindow

def main():
    root = tk.Tk()
    root.withdraw()

    db = DatabaseManager()

    def open_translator():
        root.destroy()
        exec(open("afisare.py", "r", encoding="utf-8").read(), {})

    LoginWindow(root, db, open_translator)
    root.mainloop()

if __name__ == "__main__":
    main()
