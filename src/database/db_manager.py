import sqlite3
from typing import List, Optional, Tuple
from src.models.producto import Producto
from src.models.usuario import Usuario

class DatabaseManager:
    """
    Clase que maneja todas las operaciones de la base de datos.
    Centraliza la conexión y las operaciones SQL.
    """
    def __init__(self, db_name: str = "inventario.db"):
        self.db_name = db_name
        self.inicializar_db()
        self.inicializar_db_ventas()
        self.inicializar_db_usuarios()

    def inicializar_db(self):
        """Crea la tabla de productos si no existe"""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS productos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    categoria TEXT NOT NULL,
                    precio REAL NOT NULL,
                    cantidad INTEGER NOT NULL
                )
            ''')
            
    def inicializar_db_ventas(self):
        """Crea la tabla de ventas si no existe"""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS ventas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    product_id INTEGER NOT NULL,
                    cantidad INTEGER NOT NULL,
                    fecha TEXT NOT NULL,
                    FOREIGN KEY (product_id) REFERENCES productos(id)
                )
            ''')
            
    def inicializar_db_usuarios(self):
        """Crea la tabla de usuarios si no existe"""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    contrasena TEXT NOT NULL,
                    rol TEXT NOT NULL
                )
            ''')

    def get_connection(self):
        """Obtiene una conexión a la base de datos"""
        return sqlite3.connect(self.db_name)

    def obtener_producto(self, id: int) -> Optional[Producto]:
        """Obtiene un producto por su ID"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM productos WHERE id = ?', (id,))
            resultado = cursor.fetchone()
            
            if resultado:
                return Producto(
                    id=resultado[0],
                    nombre=resultado[1],
                    categoria=resultado[2],
                    precio=resultado[3],
                    cantidad=resultado[4]
                )
            return None

    def obtener_todos_productos(self) -> List[Producto]:
        """Obtiene todos los productos de la base de datos"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM productos')
            productos = []
            for row in cursor.fetchall():
                productos.append(Producto(
                    id=row[0],
                    nombre=row[1],
                    categoria=row[2],
                    precio=row[3],
                    cantidad=row[4]
                ))
            
            return productos
        
    def obtener_busqueda(self, filtro: str, busqueda: str):
        '''obtiene uno o varios productos desde la base de datos mediante un filtro de busqueda'''
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            #busca por nombre
            if filtro == "Nombre":
                cursor.execute('''
                    SELECT * FROM productos
                    WHERE nombre LIKE ?
                    ''', (f"%{busqueda}%",))
            #busca por categoria
            elif filtro == "Categoria":
                cursor.execute('''
                    SELECT * FROM productos
                    WHERE categoria LIKE ?
                    ''', (f"%{busqueda}%",))
            #busca por rango de precios entre 0 a n
            elif filtro == "Precio":
                cursor.execute('''
                    SELECT * FROM productos
                    WHERE precio <= ?
                    ''', (busqueda,))
            else:
                return []
            
            productos = []
            for row in cursor.fetchall():
                productos.append(Producto(
                    id=row[0],
                    nombre=row[1],
                    categoria=row[2],
                    precio=row[3],
                    cantidad=row[4]
                ))
        
            return productos
        
    def insertar_producto(self, producto: Producto) -> bool:
        """Inserta un nuevo producto en la base de datos"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO productos (nombre, categoria, precio, cantidad)
                    VALUES (?, ?, ?, ?)
                ''', (producto.nombre, producto.categoria, producto.precio, producto.cantidad))
                return True
        except sqlite3.Error as e:
            print(f"Error al insertar producto: {e}")
            return False

    def actualizar_producto(self, producto: Producto) -> bool:
        """Actualiza un producto existente"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE productos 
                    SET nombre = ?, categoria = ?, precio = ?, cantidad = ?
                    WHERE id = ?
                ''', (producto.nombre, producto.categoria, producto.precio, 
                    producto.cantidad, producto.id))
                return True
        except sqlite3.Error as e:
            print(f"Error al actualizar producto: {e}")
            return False

    def eliminar_producto(self, id: int) -> bool:
        """Elimina un producto por su ID"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM productos WHERE id = ?', (id,))
                return True
        except sqlite3.Error as e:
            print(f"Error al eliminar producto: {e}")
            return False

    def verificar_nombre_existe(self, nombre: str, id_excluir: int = None) -> bool:
        """Verifica si ya existe un producto con ese nombre"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if id_excluir:
                cursor.execute('''
                    SELECT id FROM productos 
                    WHERE nombre = ? AND id != ?
                ''', (nombre, id_excluir))
            else:
                cursor.execute('SELECT id FROM productos WHERE nombre = ?', (nombre,))
            return cursor.fetchone() is not None
        
    def productos_totales(self) -> int:
        '''Obtiene el numero total de productos en la DB'''
        return len(self.obtener_todos_productos())
    
    def valor_total_inventario(self) -> float:
        '''Obtiene el valor total de todos los productos'''
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT SUM(precio) FROM productos")
            return cursor.fetchone()[0]
        
    def categorias_totales(self) -> int:
        '''Obtiene el numero total de categorias de la base de datos'''
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM productos GROUP BY categoria")
            return len(cursor.fetchall())
        
    def productos_bajos(self) -> int:
        '''obtiene los productos del stock que tiene menos de 5 unidades'''
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM productos WHERE cantidad <= 5")
            return len(cursor.fetchall())
        
    def productos_agotados(self):
        '''Obtiene los productos que estan agotados'''
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM productos WHERE cantidad = 0")
            return len(cursor.fetchall())
        
    def producto_mas_caro(self) -> dict:
        '''Obtiene el producto mas caro'''
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT nombre, max(precio) as precio FROM productos")
            resultado = cursor.fetchone()
            return {
                "nombre": resultado[0],
                "precio": resultado[1]
            }
            
            
    def producto_mas_barato(self) -> dict:
        '''Obtiene el producto mas barato'''
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT nombre, min(precio) as precio FROM productos")
            resultado = cursor.fetchone()
            return {
                "nombre": resultado[0],
                "precio": resultado[1]
            }
        
    def promedio_precios(self):
        '''Obtiene el promedio de precios de todos los productos'''
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT avg(precio) FROM productos")
            return cursor.fetchone()[0]
    
    
        
    #SECCION DE USUARIOS
    def verificar_usuario_existe(self, username: str) -> bool:
        """Verifica si ya hay un usuario existente con ese username"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                        SELECT * FROM usuarios
                        WHERE username = ?
                        ''', (username,))
            if cursor.fetchone():
                return True
            return False
    
    def crear_usuario(self, usuario: Usuario) -> bool:
        """Crea un Usuario en la base de datos"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                            INSERT INTO usuarios (username, contrasena, rol)
                            VALUES (?,?,?)
                            ''', (usuario.username, usuario.contrasena, usuario.rol))
                return True
        except sqlite3.Error as e:
            print(f"Error al crear Usuario: {e}")
            return False
        
    def login_verificacion(self, username: str, contrasena: str) -> tuple[bool,Optional[Usuario]]:
        """verifica si el usuario y la contraseña estan en la base de datos y retorna el usuario si lo encuentra"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                        SELECT * FROM usuarios
                        WHERE username = ? AND contrasena = ?
                        ''', (username, contrasena))
            resultado = cursor.fetchone()
            if resultado:
                usuario = Usuario(
                    id=resultado[0],
                    username=resultado[1],
                    contrasena=resultado[2],
                    rol=resultado[3]
                )
                return True, usuario
            return False
            