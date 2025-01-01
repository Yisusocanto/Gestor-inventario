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
    
    def obtener_busqueda(self, filtro: str, busqueda: str):
        """Obtiene un producto buscado por un filtro de la base de datos si existe"""
        return self.db.obtener_busqueda(filtro, busqueda)
    
    def productos_totales(self) -> int:
        '''Obtiene el numero total de productos en la DB'''
        return self.db.productos_totales()
    
    def valor_total_inventario(self) -> float:
        '''Obtiene el valor total de todos los productos'''
        return self.db.valor_total_inventario()
        
    def categorias_totales(self) -> int:
        '''Obtiene el numero total de categorias de la base de datos'''
        return self.db.categorias_totales()
        
    def productos_bajos(self) -> int:
        '''obtiene los productos del stock que tiene menos de 5 unidades'''
        return self.db.productos_bajos()
        
    def productos_agotados(self):
        '''Obtiene los productos que estan agotados'''
        return self.db.productos_agotados()
        
    def producto_mas_caro(self) -> dict:
        '''Obtiene el producto mas caro'''
        return self.db.producto_mas_caro()
        
    def producto_mas_barato(self) -> dict:
        '''Obtiene el producto mas barato'''
        return self.db.producto_mas_barato()
        
    def promedio_precios(self):
        '''Obtiene el proedio de precios de todos los productos'''
        return self.db.promedio_precios()