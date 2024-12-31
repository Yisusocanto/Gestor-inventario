import tkinter as tk
from tkinter import ttk, messagebox
from src.controllers.producto_controller import ProductoController
from src.controllers.venta_controller import VentaController

class MainWindow:
    """Ventana principal de la aplicación"""
    
    def __init__(self):
        self.ventana = tk.Tk()
        self.producto_controller = ProductoController()
        self.venta_controller = VentaController()
        self.configurar_ventana()
        self.crear_widgets()
        self.actualizar_treeview()

    def configurar_ventana(self):
        """Configura las propiedades básicas de la ventana"""
        self.ventana.title("Gestor de Inventario")
        self.ventana.geometry("1000x700")

    def crear_widgets(self):
        """Crea todos los widgets de la interfaz"""
        # Frame para entrada de datos
        self.frame_entrada = tk.Frame(self.ventana)
        self.frame_entrada.pack(pady=10)

        # Campos de entrada
        self.crear_campos_entrada()

        # Frame para botones
        self.frame_botones = tk.Frame(self.ventana)
        self.frame_botones.pack(pady=5)

        # Botones
        self.crear_botones()
        
        #frame para busquedas
        self.frame_busqueda = tk.Frame(self.ventana)
        self.frame_busqueda.pack(pady=10)
        
        #campos de busqueda
        self.crear_campos_busqueda()

        # Treeview
        self.crear_treeview()

    def crear_campos_entrada(self):
        """Crea los campos de entrada de datos"""
        # Labels y entries
        labels = ['Nombre', 'Categoría', 'Precio', 'Cantidad']
        self.entries = {}

        for i, label in enumerate(labels):
            tk.Label(self.frame_entrada, text=label).grid(row=0, column=i, padx=5, pady=5)
            entry = tk.Entry(self.frame_entrada)
            entry.grid(row=1, column=i, padx=5, pady=5)
            self.entries[label.lower()] = entry
            
    def crear_campos_busqueda(self):
        '''Crea todos los campos (label, entry, combobox y boton) del apartado de busqueda de producto'''
        label_busqueda = tk.Label(self.frame_busqueda, text="Buscar producto por:")
        label_busqueda.pack(side=tk.LEFT, padx=5)
        
        # Guarda la referencia al Combobox
        self.opciones_busqueda = ttk.Combobox(
            self.frame_busqueda,
            values=["nombre", "categoria", "precio"])
        self.opciones_busqueda.pack(side=tk.LEFT, padx=5)
        
        # Guarda la referencia al Entry
        self.entry_busqueda = tk.Entry(self.frame_busqueda)
        self.entry_busqueda.pack(side=tk.LEFT, padx=5)
        
        boton_busqueda = tk.Button(
            self.frame_busqueda, 
            text="BUSCAR", 
            command=self.actualizar_treeview_busqueda
        )
        boton_busqueda.pack(side=tk.LEFT, padx=5)

    def crear_botones(self):
        """Crea los botones de acción"""
        botones = [
            ("Crear", self.crear_producto),
            ("Eliminar", self.eliminar_producto),
            ("Editar", self.editar_producto),
            ("Vender", self.mostrar_ventana_ventas),
            ("Refrescar", self.actualizar_treeview)
        ]

        for texto, comando in botones:
            tk.Button(self.frame_botones, text=texto, command=comando).pack(side=tk.LEFT, padx=5)

    def crear_treeview(self):
        """Crea y configura el Treeview"""
        columnas = ("id", "nombre", "categoria", "precio", "cantidad")
        self.tree = ttk.Treeview(self.ventana, columns=columnas, show="headings")

        # Configurar columnas
        for col in columnas:
            self.tree.heading(col, text=col.title())
            self.tree.column(col, width=100)

        self.tree.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    def actualizar_treeview(self):
        """Actualiza el contenido del Treeview"""
        # Limpiar treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Insertar productos
        for producto in self.producto_controller.obtener_todos_productos():
            self.tree.insert("", "end", values=(
                producto.id,
                producto.nombre,
                producto.categoria,
                producto.precio,
                producto.cantidad
            ))
            
    def actualizar_treeview_busqueda(self):
        '''Actualiza el treeview con el producto buscado cuando se clickea el boton buscar'''
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        filtro = self.opciones_busqueda.get().capitalize()
        busqueda = self.entry_busqueda.get().capitalize()

        productos = self.producto_controller.obtener_busqueda(filtro, busqueda)
        if productos:
            for producto in productos:
                self.tree.insert("", "end", values=(
                producto.id,
                producto.nombre,
                producto.categoria,
                producto.precio,
                producto.cantidad
                ))
                

    def crear_producto(self):
        """Maneja la creación de un nuevo producto"""
        valores = {
            'nombre': self.entries['nombre'].get(),
            'categoria': self.entries['categoría'].get(),
            'precio': self.entries['precio'].get(),
            'cantidad': self.entries['cantidad'].get()
        }

        exito, mensaje = self.producto_controller.crear_producto(**valores)
        
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self.limpiar_campos()
            self.actualizar_treeview()
        else:
            messagebox.showerror("Error", mensaje)

    def eliminar_producto(self):
        """Maneja la eliminación de un producto"""
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor, seleccione un producto")
            return

        if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar el producto?"):
            item = self.tree.item(seleccion[0])
            id_producto = item['values'][0]
            
            exito, mensaje = self.producto_controller.eliminar_producto(id_producto)
            
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                self.actualizar_treeview()
            else:
                messagebox.showerror("Error", mensaje)

    def editar_producto(self):
        """Maneja la edición de un producto"""
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor, seleccione un producto")
            return

        item = self.tree.item(seleccion[0])
        id_producto = item['values'][0]

        valores = {
            'id': id_producto,
            'nombre': self.entries['nombre'].get(),
            'categoria': self.entries['categoría'].get(),
            'precio': self.entries['precio'].get(),
            'cantidad': self.entries['cantidad'].get()
        }

        exito, mensaje = self.producto_controller.actualizar_producto(**valores)
        
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self.limpiar_campos()
            self.actualizar_treeview()
        else:
            messagebox.showerror("Error", mensaje)

    def mostrar_ventana_ventas(self):
        """Abre la ventana de ventas"""
        from src.views.ventas_window import VentasWindow
        VentasWindow(self)

    def limpiar_campos(self):
        """Limpia todos los campos de entrada"""
        for entry in self.entries.values():
            entry.delete(0, tk.END)

    def iniciar(self):
        """Inicia la aplicación"""
        self.ventana.mainloop()