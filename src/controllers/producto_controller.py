from typing import List, Optional, Tuple
from src.models.producto import Producto
from src.database.db_manager import DatabaseManager

class ProductoController:
    """Controlador que maneja la lógica de negocio relacionada con productos."""
    
    def __init__(self):
        self.db = DatabaseManager()

    def crear_producto(self, nombre: str, categoria: str, precio: str, cantidad: str) -> Tuple[bool, str]:
        try:
            if not all([nombre, categoria, precio, cantidad]):
                return False, "Todos los campos son requeridos"

            precio_float = float(precio)
            cantidad_int = int(cantidad)

            if precio_float < 0:
                return False, "El precio no puede ser negativo"
            if cantidad_int < 0:
                return False, "La cantidad no puede ser negativa"

            if self.db.verificar_nombre_existe(nombre):
                return False, "Ya existe un producto con ese nombre"

            nuevo_producto = Producto(
                nombre=nombre.capitalize(),
                categoria=categoria.capitalize(),
                precio=precio_float,
                cantidad=cantidad_int
            )

            if self.db.insertar_producto(nuevo_producto):
                return True, "Producto creado exitosamente"
            return False, "Error al guardar en la base de datos"

        except ValueError:
            return False, "El precio y la cantidad deben ser números válidos"
        except Exception as e:
            return False, f"Error inesperado: {str(e)}"

    def actualizar_producto(self, id: int, nombre: str, categoria: str, 
                          precio: str, cantidad: str) -> Tuple[bool, str]:
        try:
            if not all([nombre, categoria, precio, cantidad]):
                return False, "Todos los campos son requeridos"

            precio_float = float(precio)
            cantidad_int = int(cantidad)

            if precio_float < 0:
                return False, "El precio no puede ser negativo"
            if cantidad_int < 0:
                return False, "La cantidad no puede ser negativa"

            if self.db.verificar_nombre_existe(nombre, id_excluir=id):
                return False, "Ya existe otro producto con ese nombre"

            producto = Producto(
                id=id,
                nombre=nombre.capitalize(),
                categoria=categoria.capitalize(),
                precio=precio_float,
                cantidad=cantidad_int
            )

            if self.db.actualizar_producto(producto):
                return True, "Producto actualizado exitosamente"
            return False, "No se pudo actualizar el producto"

        except ValueError:
            return False, "El precio y la cantidad deben ser números válidos"
        except Exception as e:
            return False, f"Error al actualizar: {str(e)}"

    def eliminar_producto(self, id: int) -> Tuple[bool, str]:
        try:
            if self.db.eliminar_producto(id):
                return True, "Producto eliminado exitosamente"
            return False, "No se pudo eliminar el producto"
        except Exception as e:
            return False, f"Error al eliminar: {str(e)}"

    def obtener_producto(self, id: int) -> Optional[Producto]:
        """Obtiene un producto por su ID"""
        return self.db.obtener_producto(id)

    def obtener_todos_productos(self) -> List[Producto]:
        """Obtiene todos los productos"""
        return self.db.obtener_todos_productos()