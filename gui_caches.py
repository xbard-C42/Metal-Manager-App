import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import webbrowser
from db_caches import init_caches_table, list_caches, add_cache
from map_utils import generate_cache_map

class CacheManagerFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        init_caches_table()
        self.create_widgets()

    def create_widgets(self):
        cols = ('ID', 'Name', 'Latitude', 'Longitude', 'Description')
        self.tree = ttk.Treeview(self, columns=cols, show='headings')
        for c in cols:
            self.tree.heading(c, text=c)
        self.tree.pack(fill='both', expand=True, side='left')
        ctrl = ttk.Frame(self)
        ctrl.pack(side='right', fill='y', padx=5)
        ttk.Button(ctrl, text="Add Cache", command=self.add_cache_dialog).pack(pady=2)
        ttk.Button(ctrl, text="Show Map", command=self.show_map).pack(pady=2)
        self.populate()

    def populate(self):
        for r in self.tree.get_children():
            self.tree.delete(r)
        for row in list_caches():
            self.tree.insert('', 'end', values=row)

    def add_cache_dialog(self):
        name = simpledialog.askstring("Cache Name", "Enter cache name:")
        if not name: return
        lat = simpledialog.askfloat("Latitude", "Enter latitude:")
        lng = simpledialog.askfloat("Longitude", "Enter longitude:")
        desc = simpledialog.askstring("Description", "Enter description (optional):")
        add_cache(name, lat, lng, desc)
        self.populate()

    def show_map(self):
        caches = list_caches()
        if not caches:
            messagebox.showinfo("No Caches", "No caches to map.")
            return
        avg_lat = sum(c[2] for c in caches)/len(caches)
        avg_lng = sum(c[3] for c in caches)/len(caches)
        path = generate_cache_map(caches, default_location=(avg_lat, avg_lng), zoom=8)
        webbrowser.open(path)