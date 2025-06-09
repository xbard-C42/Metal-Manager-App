"""
Silver Add-On GUI Extension: Adds a Silver tab to the main app.
"""
from tkinter import ttk
from api import fetch_price
from db import list_bars

class SilverTab:
    def integrate(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Silver")
        price = fetch_price("XAG")
        ttk.Label(frame, text=f"Current Silver Price (USD): {price:.4f}").pack(pady=10)
        cols = ('ID','Weight','Purity','Location','Acquired')
        tree = ttk.Treeview(frame, columns=cols, show='headings')
        for c in cols:
            tree.heading(c, text=c)
        for r in list_bars():
            if r[5] == 'silver':
                tree.insert('', 'end', values=r)
        tree.pack(fill='both', expand=True)