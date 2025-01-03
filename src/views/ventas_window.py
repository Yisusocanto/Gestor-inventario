import tkinter as tk
from tkinter import ttk, messagebox

class VentasWindow:
    """Ventana para realizar ventas"""

    def __init__(self, parent):
        self.parent = parent
        self.ventana = tk.Toplevel(parent.ventana)
        self.configurar_ventana()
        self.crear_widgets()
        self.actualizar_treeview()

    def configurar_ventana(self):
        """Configura las propiedades de la ventana"""
        self.ventana.title("Realizar Venta")
        self.ventana.geometry("800x600")

    def crear_widgets(self):
        """Crea los widgets de la ventana"""
        # Frame superior
        frame_superior = tk.Frame(self.ventana)
        frame_superior.pack(pady=10)

        # Campo cantidad
        tk.Label(frame_superior, text="Cantidad:").pack(side=tk.LEFT, padx=5)
        self.cantidad_entry = tk.Entry(frame_superior)
        self.cantidad_entry.pack(side=tk.LEFT, padx=5)

        # Botón vender
        tk.Button(frame_superior, text="Realizar Venta", 
                command=self.realizar_venta).pack(side=tk.LEFT, padx=5)

        # Treeview
        self.crear_treeview()

    def crear_treeview(self):
        """Crea y configura el Treeview"""
        columnas = ("id", "nombre", "categoria", "precio", "cantidad")
        self.tree = ttk.Treeview(self.ventana, columns=columnas, show="headings")

        for col in columnas:
            self.tree.heading(col, text=col.title())
            self.tree.column(col, width=100)

        self.tree.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    def actualizar_treeview(self):
        """Actualiza el contenido del Treeview"""
        for item in self.tree.get_children():
            self.tree.delete(item)

        for producto in self.parent.producto_controller.obtener_todos_productos():
            self.tree.insert("", "end", values=(
                producto.id,
                producto.nombre,
                producto.categoria,
                producto.precio,
                producto.cantidad
            ))

    def realizar_venta(self):
        """Procesa la venta del producto seleccionado"""
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor, seleccione un producto")
            return

        try:
            cantidad = int(self.cantidad_entry.get())
            if cantidad <= 0:
                messagebox.showwarning("Error", "La cantidad debe ser mayor a 0")
                return
        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un número válido")
            return

        item = self.tree.item(seleccion[0])
        id_producto = item['values'][0]

        exito, mensaje = self.parent.venta_controller.realizar_venta(id_producto, cantidad)
        
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self.parent.actualizar_treeview()
            self.actualizar_treeview()
            self.ventana.destroy()
        else:
            messagebox.showerror("Error", mensaje)