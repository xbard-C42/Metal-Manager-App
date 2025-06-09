"""
Gold Add-On GUI Extension: Adds a Gold tab to the main app.
"""
from tkinter import ttk
from api import fetch_price
from db import list_bars

class GoldTab:
    def integrate(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Gold")
        price = fetch_price("XAU")
        ttk.Label(frame, text=f"Current Gold Price (USD): {price:.4f}").pack(pady=10)
        cols = ('ID','Weight','Purity','Location','Acquired')
        tree = ttk.Treeview(frame, columns=cols, show='headings')
        for c in cols:
            tree.heading(c, text=c)
        for r in list_bars():
            if r[5] == 'gold':
                tree.insert('', 'end', values=r)
        tree.pack(fill='both', expand=True)