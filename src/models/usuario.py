class Usuario:
    """
    Clase que representa los usuarios en la base de datos que pueden usar el Gestor.
    Solo contiene la estructura de datos, no la lógica de negocio.
    """
    def __init__(self, id=None, username="", contrasena="", rol="vendedor"):
        self.id = id
        self.username = username
        self.contrasena = contrasena
        self.rol = rol
        
    def __str__(self):
        return f"Nombre: {self.username} ({self.rol}) - Contreseña: {self.contrasena})"