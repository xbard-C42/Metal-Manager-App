import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from config import verify_pin, set_pin, load_config
from db import init_db, add_bar, list_bars
from api import fetch_metal_price
from plugins import discover_plugins
from gui_caches import CacheManagerFrame

class CopperManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Copper Manager Pro")
        self.geometry("800x600")
        if not self.authenticate():
            self.destroy()
            return
        init_db()
        self.plugins = discover_plugins()
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='both', expand=True)
        self.build_tabs()

    def authenticate(self):
        cfg = load_config()
        if cfg.get('pin_hash') is None:
            pin = simpledialog.askstring("Set PIN", "No PIN set. Enter new PIN:", show='*')
            confirm = simpledialog.askstring("Confirm PIN", "Confirm new PIN:", show='*')
            if pin and pin == confirm:
                set_pin(pin)
            else:
                messagebox.showerror("Error", "PINs did not match. Exiting.")
                return False
        for _ in range(3):
            attempt = simpledialog.askstring("PIN", "Enter your manager PIN:", show='*')
            if verify_pin(attempt):
                return True
            messagebox.showwarning("Invalid PIN", "Invalid PIN, try again.")
        messagebox.showerror("Error", "Too many failed attempts.")
        return False

    def build_tabs(self):
        # Copper Tab
        self.build_metal_tab('Copper', 'copper')
        # Plugin Tabs
        for p in self.plugins:
            if p.get('enabled'):
                key = p['symbol'].lower()
                self.build_metal_tab(p['name'], key)
        # Caches Tab
        cache_tab = CacheManagerFrame(self.notebook)
        self.notebook.add(cache_tab, text="Caches")

    def build_metal_tab(self, title, metal_key):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text=title)
        price = fetch_metal_price(metal_key)
        ttk.Label(frame, text=f"Current {title} Price (USD): {price:.4f}").pack(pady=10)
        cols = ('ID','Weight','Purity','Location','Acquired','Cache_ID')
        tree = ttk.Treeview(frame, columns=cols, show='headings')
        for c in cols:
            tree.heading(c, text=c)
        for r in list_bars():
            if r[5] == metal_key:
                tree.insert('', 'end', values=(r[0], r[1], r[2], r[3], r[4], r[6]))
        tree.pack(fill='both', expand=True)