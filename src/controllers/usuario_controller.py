from typing import List, Optional, Tuple
from src.models.usuario import Usuario
from src.database.db_manager import DatabaseManager

class UsuarioController:
    """Controlador que maneja toda la logica de negocio de los usuarios"""
    
    def __init__(self):
        self.db = DatabaseManager()
        
    def crear_usuario(self, username: str, contrasena: str, rol: str, clave_admin: str) -> Tuple[bool, str]:
        """Trata crear el producto, retorna un valor booleano y un mensaje dependiendo si se falla o es exitoso"""        
        try:
            if not all([username, contrasena, rol, clave_admin]):
                return False, "Todos los campos son requeridos."
            
            if len(contrasena) < 8:
                return False, "La contraseña debe tener 8 o mas caracteres."
            
            if self.db.verificar_usuario_existe(username):
                return False, "El usuario ya existe."
            
            if clave_admin == "1234567890": #clave especial de administrador/gerente estatica para crear nuevos usuarios
                nuevo_usuario = Usuario(
                    username=username,
                    contrasena=contrasena,
                    rol=rol
                )
                if self.db.crear_usuario(nuevo_usuario):
                    return True, "Usuario creado Exitosamente."
                return False, "Fallo al crear el usuario."
            else:
                return False, "La clave de administrador es incorrecta."        
        except Exception as e:
            print("Error inesperado", e)
            return False, "Ha ocurrido un error inesperado."
        
    
    def login_verificacion(self, username: str, contrasena: str) -> Tuple[bool, str, Optional[Usuario]]:
        """Verifica si el usuario y la contraseña estan en la base de datos y devuelve una tupla con un booleano, un mensaje de exito o fallo y el usuario"""
        try:
            if not all([username, contrasena]):
                return False, "Todos los campos son requeridos.", None
            
            resultado = self.db.login_verificacion(username, contrasena)
            if resultado:
                return True, "Sesion Iniciada.", resultado[1]
            return False, "Usuario no encontrado o contraseña incorrecta.", None
        except Exception as e:
            print("Error inesperado", e)
            return False, "Ha ocurrido un error inesperado.", None
        
        