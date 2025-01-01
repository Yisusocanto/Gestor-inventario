import tkinter as tk
from tkinter import ttk, messagebox

class ReportesWindow:
    def __init__(self, parent):
        self.parent = parent
        self.ventana = tk.Toplevel()
        self.configurar_ventana()
        self.crear_widgets()
        
    def configurar_ventana(self):
        """Configura las propiedades de la ventana"""
        self.ventana.title("Reporte de Inventario")
        self.ventana.geometry("800x600")

    def crear_widgets(self):
        """Crea los widgets de la ventana"""
        # Frame principal
        frame_principal = tk.Frame(self.ventana)
        frame_principal.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        # Frame Resumen General
        frame_resumen_general = tk.LabelFrame(frame_principal, text="Resumen General")
        frame_resumen_general.pack(pady=10, fill=tk.X)
        
        # Labels resumen general
        self.labels_resumen_general(frame_resumen_general)
        
        # Frame Stock
        frame_stock = tk.LabelFrame(frame_principal, text="Stock")
        frame_stock.pack(pady=10, fill=tk.X)
        
        # Labels de stock
        self.labels_stock(frame_stock)
        
        # Frame Valorización
        frame_valorizacion = tk.LabelFrame(frame_principal, text="Valorización")
        frame_valorizacion.pack(pady=10, fill=tk.X)
        
        # Labels de valorización
        self.labels_valorizacion(frame_valorizacion)
        
        # Frame botones
        frame_botones = tk.Frame(frame_principal)
        frame_botones.pack(side=tk.BOTTOM, pady=10)
        
        # Botones
        btn_exportar = tk.Button(frame_botones, text="Exportar", command=self.exportar_reporte)
        btn_exportar.pack(side=tk.LEFT, padx=5)
        
        btn_cerrar = tk.Button(frame_botones, text="Cerrar", command=self.ventana.destroy)
        btn_cerrar.pack(side=tk.LEFT, padx=5)

    def labels_resumen_general(self, frame):
        """Crea labels para el resumen general"""
        datos_resumen = [
            ("Total Productos:", self.parent.producto_controller.productos_totales()),
            ("Valor Total Inventario:", f"{self.parent.producto_controller.valor_total_inventario()}$"),
            ("Número de Categorías:", self.parent.producto_controller.categorias_totales())
        ]
        
        for i, (etiqueta, valor) in enumerate(datos_resumen):
            label = tk.Label(frame, text=f"{etiqueta} {valor}")
            label.pack(anchor='w', padx=10, pady=5)

    def labels_stock(self, frame):
        """Crea labels para información de stock"""
        datos_stock = [
            ("Productos con Stock Bajo:", self.parent.producto_controller.productos_bajos()),
            ("Productos Agotados:", self.parent.producto_controller.productos_agotados())
        ]
        
        for etiqueta, valor in datos_stock:
            label = tk.Label(frame, text=f"{etiqueta} {valor}")
            label.pack(anchor='w', padx=10, pady=5)

    def labels_valorizacion(self, frame):
        """Crea labels para valorización"""
        datos_valorizacion = [
            ("Producto Más Caro:", f"{self.parent.producto_controller.producto_mas_caro()["nombre"]}: {self.parent.producto_controller.producto_mas_caro()["precio"]}$"),
            ("Producto Más Barato:", f"{self.parent.producto_controller.producto_mas_barato()["nombre"]}: {self.parent.producto_controller.producto_mas_barato()["precio"]}$"),
            ("Precio Promedio:", f"{self.parent.producto_controller.promedio_precios()}$")
        ]
        
        for etiqueta, valor in datos_valorizacion:
            label = tk.Label(frame, text=f"{etiqueta} {valor}")
            label.pack(anchor='w', padx=10, pady=5)

    def exportar_reporte(self):
        """Método para exportar el reporte"""
        messagebox.showinfo("Exportar", "Funcionalidad de exportación próximamente")