class Producto:
    """
    Clase que representa un producto en el inventario.
    Solo contiene la estructura de datos, no la lógica de negocio.
    """
    def __init__(self, id=None, nombre="", categoria="", precio=0, cantidad=0):
        self.id = id
        self.nombre = nombre
        self.categoria = categoria
        self.precio = precio
        self.cantidad = cantidad

    def __str__(self):
        return f"Producto: {self.nombre} ({self.categoria}) - ${self.precio} - Stock: {self.cantidad}"