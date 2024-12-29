import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


# Constantes
DB_NAME = "inventario.db"
WINDOW_SIZE = "1000x700"
PADDING = {'padx': 4, 'pady': 4}


class VentanaRegistro:
    def __init__(self, parent):
        self.parent = parent
        self.ventana = tk.Toplevel()
        self.title = "Registro de Ventas"
        self.geometry = WINDOW_SIZE
        self.crear_componentes()
        
    def crear_componentes(self):
        """Crea los componentes de la ventana registro de ventas"""
        self.tree_registro = ttk.Treeview(self.ventana, columns=("id", "nombre", "cantidad"), show="headings")
        
        for col in self.tree_registro["columns"]:
            self.tree_registro.heading(col, text=col.upper())
            
        self.tree_registro.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        self.parent.update_treeview_registro(self.tree_registro)