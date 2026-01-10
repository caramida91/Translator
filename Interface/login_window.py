import tkinter as tk
from tkinter import ttk, messagebox

class LoginWindow:
    def __init__(self, root, db, on_success):
        self.root = root
        self.db = db
        self.on_success = on_success

        self.win = tk.Toplevel(root)
        self.win.title("Login")
        self.win.geometry("300x250")

        ttk.Label(self.win, text="Username:").pack(pady=5)
        self.entry_user = ttk.Entry(self.win)
        self.entry_user.pack()

        ttk.Label(self.win, text="Password:").pack(pady=5)
        self.entry_pass = ttk.Entry(self.win, show="*")
        self.entry_pass.pack()

        ttk.Button(self.win, text="Login", command=self.login).pack(pady=10)
        ttk.Button(self.win, text="Register", command=self.register).pack()

    def login(self):
        user = self.entry_user.get()
        pwd = self.entry_pass.get()

        if self.db.login_user(user, pwd):
            messagebox.showinfo("Succes", "Login reușit!")
            self.win.destroy()
            self.on_success()
        else:
            messagebox.showerror("Eroare", "User sau parolă greșită!")

    def register(self):
        user = self.entry_user.get()
        pwd = self.entry_pass.get()

        if self.db.register_user(user, pwd):
            messagebox.showinfo("Succes", "Cont creat!")
        else:
            messagebox.showerror("Eroare", "User deja există!")
