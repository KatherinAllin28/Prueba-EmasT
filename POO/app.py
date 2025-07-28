import sqlite3
from datetime import datetime, timedelta
import os # Importar el módulo os para manejar archivos

class Item:
    def __init__(self, titulo: str, autor_editor: str, anio_publicacion: int, cantidad_total: int):
        self._titulo = titulo
        self._autor_editor = autor_editor
        self._anio_publicacion = anio_publicacion
        self._cantidad_total = cantidad_total
        self._cantidad_disponible = cantidad_total # Inicialmente, todos los ítems están disponibles

    @property
    def titulo(self) -> str:
        return self._titulo

    @property
    def autor_editor(self) -> str:
        return self._autor_editor

    @property
    def anio_publicacion(self) -> int:
        return self._anio_publicacion

    @property
    def cantidad_total(self) -> int:
        return self._cantidad_total

    @property
    def cantidad_disponible(self) -> int:
        return self._cantidad_disponible

    def incrementar_disponible(self):
        if self._cantidad_disponible < self._cantidad_total:
            self._cantidad_disponible += 1
            return True
        return False

    def decrementar_disponible(self):
        if self._cantidad_disponible > 0:
            self._cantidad_disponible -= 1
            return True
        return False

    def mostrar_info(self) -> str:
        return (f"Título: {self.titulo}, Autor/Editor: {self.autor_editor}, "
                f"Año: {self.anio_publicacion}, Disponible: {self.cantidad_disponible}/{self.cantidad_total}")

class Libro(Item):
    def __init__(self, titulo: str, autor: str, anio_publicacion: int, isbn: str, cantidad_total: int):
        super().__init__(titulo, autor, anio_publicacion, cantidad_total)
        self._isbn = isbn # Atributo específico de Libro

    @property
    def isbn(self) -> str:
        return self._isbn

    def mostrar_info(self) -> str:
        return (f"Libro: {self.titulo}, Autor: {self.autor_editor}, Año: {self.anio_publicacion}, "
                f"ISBN: {self.isbn}, Disponible: {self.cantidad_disponible}/{self.cantidad_total}")

class Revista(Item):
    def __init__(self, titulo: str, editor: str, anio_publicacion: int, numero: int, cantidad_total: int):
        super().__init__(titulo, editor, anio_publicacion, cantidad_total)
        self._numero = numero # Atributo específico de Revista

    @property
    def numero(self) -> int:
        return self._numero

    def mostrar_info(self) -> str:
        return (f"Revista: {self.titulo}, Editor: {self.autor_editor}, Año: {self.anio_publicacion}, "
                f"Número: {self.numero}, Disponible: {self.cantidad_disponible}/{self.cantidad_total}")


class Biblioteca:
    def __init__(self, db_name: str = 'biblioteca.db'):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self._conectar_db()
        self._crear_tablas()

    def _conectar_db(self):
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            print(f"Conectado a la base de datos: {self.db_name}")
        except sqlite3.Error as e:
            print(f"Error al conectar a la base de datos: {e}")

    def _crear_tablas(self):
        if self.cursor is None:
            print("No hay conexión a la base de datos para crear tablas.")
            return

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo TEXT NOT NULL,
                titulo TEXT NOT NULL,
                autor_editor TEXT NOT NULL,
                anio_publicacion INTEGER NOT NULL,
                identificador_unico TEXT,
                cantidad_total INTEGER NOT NULL,
                cantidad_disponible INTEGER NOT NULL
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS prestamos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_id INTEGER NOT NULL,
                fecha_prestamo TEXT NOT NULL,
                fecha_devolucion_esperada TEXT NOT NULL,
                fecha_devolucion_real TEXT,
                prestatario TEXT NOT NULL,
                FOREIGN KEY (item_id) REFERENCES items(id)
            )
        ''')
        self.conn.commit()
        print("Tablas 'items' y 'prestamos' verificadas/creadas.")


    def agregar_item(self, item: Item):
        if self.cursor is None:
            print("No hay conexión a la base de datos.")
            return

        tipo = ""
        identificador_unico = None
        if isinstance(item, Libro):
            tipo = "Libro"
            identificador_unico = item.isbn
        elif isinstance(item, Revista):
            tipo = "Revista"
            identificador_unico = str(item.numero)
        else:
            print("Tipo de ítem no soportado.")
            return

        try:
            self.cursor.execute('''
                INSERT INTO items (tipo, titulo, autor_editor, anio_publicacion, identificador_unico, cantidad_total, cantidad_disponible)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (tipo, item.titulo, item.autor_editor, item.anio_publicacion, identificador_unico, item.cantidad_total, item.cantidad_disponible))
            self.conn.commit()
            print(f"Ítem '{item.titulo}' agregado exitosamente.")
        except sqlite3.Error as e:
            print(f"Error al agregar ítem: {e}")

    def prestar_item(self, item_id: int, prestatario: str) -> bool:
        if self.cursor is None:
            print("No hay conexión a la base de datos.")
            return False

        try:
            self.cursor.execute("SELECT cantidad_disponible, titulo FROM items WHERE id = ?", (item_id,))
            result = self.cursor.fetchone()

            if result is None:
                print(f"Error: Ítem con ID {item_id} no encontrado.")
                return False

            cantidad_disponible, titulo_item = result
            if cantidad_disponible <= 0:
                print(f"El ítem '{titulo_item}' (ID: {item_id}) no está disponible para préstamo.")
                return False

            self.cursor.execute("UPDATE items SET cantidad_disponible = cantidad_disponible - 1 WHERE id = ?", (item_id,))

            fecha_prestamo = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            fecha_devolucion_esperada = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d %H:%M:%S")

            self.cursor.execute('''
                INSERT INTO prestamos (item_id, fecha_prestamo, fecha_devolucion_esperada, prestatario)
                VALUES (?, ?, ?, ?)
            ''', (item_id, fecha_prestamo, fecha_devolucion_esperada, prestatario))

            self.conn.commit()
            print(f"'{titulo_item}' (ID: {item_id}) prestado a '{prestatario}' exitosamente.")
            return True
        except sqlite3.Error as e:
            print(f"Error al prestar ítem: {e}")
            self.conn.rollback() # Deshacer cambios si hay un error
            return False

    def devolver_item(self, prestamo_id: int) -> bool:
        if self.cursor is None:
            print("No hay conexión a la base de datos.")
            return False

        try:
            self.cursor.execute("SELECT item_id, fecha_devolucion_real FROM prestamos WHERE id = ?", (prestamo_id,))
            prestamo_info = self.cursor.fetchone()

            if prestamo_info is None:
                print(f"Error: Préstamo con ID {prestamo_id} no encontrado.")
                return False

            item_id, fecha_devolucion_real = prestamo_info
            if fecha_devolucion_real is not None:
                print(f"El préstamo con ID {prestamo_id} ya ha sido devuelto.")
                return False

            fecha_devolucion_real = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.cursor.execute('''
                UPDATE prestamos SET fecha_devolucion_real = ? WHERE id = ?
            ''', (fecha_devolucion_real, prestamo_id))

            self.cursor.execute("UPDATE items SET cantidad_disponible = cantidad_disponible + 1 WHERE id = ?", (item_id,))

            self.conn.commit()
            print(f"Préstamo con ID {prestamo_id} devuelto exitosamente. Ítem ID: {item_id}.")
            return True
        except sqlite3.Error as e:
            print(f"Error al devolver ítem: {e}")
            self.conn.rollback()
            return False

    def listar_items_disponibles(self):
        """
        Lista todos los ítems que tienen cantidad_disponible > 0.
        """
        if self.cursor is None:
            print("No hay conexión a la base de datos.")
            return []

        print("\n--- Ítems Disponibles ---")
        try:
            self.cursor.execute("SELECT id, tipo, titulo, autor_editor, cantidad_disponible FROM items WHERE cantidad_disponible > 0")
            items = self.cursor.fetchall()
            if not items:
                print("No hay ítems disponibles en este momento.")
                return []
            for item in items:
                print(f"ID: {item[0]}, Tipo: {item[1]}, Título: '{item[2]}', Autor/Editor: {item[3]}, Disponibles: {item[4]}")
            return items
        except sqlite3.Error as e:
            print(f"Error al listar ítems disponibles: {e}")
            return []

    def encontrar_items_prestados_actualmente(self):
        """
        Encuentra los ítems que están prestados actualmente (fecha_devolucion_real es NULL).
        """
        if self.cursor is None:
            print("No hay conexión a la base de datos.")
            return []

        print("\n--- Ítems Prestados Actualmente ---")
        try:
            self.cursor.execute('''
                SELECT p.id, i.titulo, i.tipo, p.prestatario, p.fecha_prestamo, p.fecha_devolucion_esperada
                FROM prestamos p
                JOIN items i ON p.item_id = i.id
                WHERE p.fecha_devolucion_real IS NULL
            ''')
            prestamos = self.cursor.fetchall()
            if not prestamos:
                print("No hay ítems prestados actualmente.")
                return []
            for prestamo in prestamos:
                print(f"Préstamo ID: {prestamo[0]}, Título: '{prestamo[1]}', Tipo: {prestamo[2]}, "
                      f"Prestatario: {prestamo[3]}, Fecha Préstamo: {prestamo[4]}, "
                      f"Devolución Esperada: {prestamo[5]}")
            return prestamos
        except sqlite3.Error as e:
            print(f"Error al encontrar ítems prestados: {e}")
            return []

    def calcular_item_mas_prestado(self):
        """
        Calcula el ítem que ha sido prestado más veces.
        """
        if self.cursor is None:
            print("No hay conexión a la base de datos.")
            return None

        print("\n--- Ítem Más Prestado ---")
        try:
            self.cursor.execute('''
                SELECT i.titulo, i.tipo, COUNT(p.item_id) AS total_prestamos
                FROM prestamos p
                JOIN items i ON p.item_id = i.id
                GROUP BY p.item_id
                ORDER BY total_prestamos DESC
                LIMIT 1
            ''')
            mas_prestado = self.cursor.fetchone()
            if mas_prestado:
                print(f"El ítem más prestado es: '{mas_prestado[0]}' ({mas_prestado[1]}) con {mas_prestado[2]} préstamos.")
                return mas_prestado
            else:
                print("No hay registros de préstamos para determinar el ítem más prestado.")
                return None
        except sqlite3.Error as e:
            print(f"Error al calcular el ítem más prestado: {e}")
            return None

    def cerrar_db(self):
        """Cierra la conexión con la base de datos."""
        if self.conn:
            self.conn.close()
            print("Conexión a la base de datos cerrada.")

# --- Ejemplo de Uso ---
if __name__ == "__main__":
    if os.path.exists('biblioteca.db'):
        os.remove('biblioteca.db')
        print("Base de datos anterior eliminada para un inicio limpio.")

    biblioteca = Biblioteca()

    print("\n--- Agregando ítems ---")
    libro1 = Libro("Cien Años de Soledad", "Gabriel García Márquez", 1967, "978-0307474728", 3)
    libro2 = Libro("1984", "George Orwell", 1949, "978-0451524935", 2)
    revista1 = Revista("National Geographic", "National Geographic Society", 2023, 10, 5)
    revista2 = Revista("Scientific American", "Springer Nature", 2024, 1, 1)

    biblioteca.agregar_item(libro1)
    biblioteca.agregar_item(libro2)
    biblioteca.agregar_item(revista1)
    biblioteca.agregar_item(revista2)

    print("\n--- Información de Ítems (Polimorfismo) ---")
    print(libro1.mostrar_info())
    print(revista1.mostrar_info())

    print("\n--- Estado Inicial de la Biblioteca ---")
    biblioteca.listar_items_disponibles()
    biblioteca.encontrar_items_prestados_actualmente()
    biblioteca.calcular_item_mas_prestado()

    print("\n--- Realizando préstamos ---")
    biblioteca.prestar_item(1, "Juan Pérez") # Cien Años de Soledad (ID 1)
    biblioteca.prestar_item(1, "Ana García") # Cien Años de Soledad (ID 1, otra copia)
    biblioteca.prestar_item(3, "Carlos Ruiz") # National Geographic (ID 3)
    biblioteca.prestar_item(2, "Laura Martínez") # 1984 (ID 2)
    biblioteca.prestar_item(2, "Pedro Sánchez") # 1984 (ID 2, segunda copia)
    biblioteca.prestar_item(2, "María López") # Intentar prestar 1984, debería decir no disponible

    print("\n--- Estado de la Biblioteca después de Préstamos ---")
    biblioteca.listar_items_disponibles()
    biblioteca.encontrar_items_prestados_actualmente()
    biblioteca.calcular_item_mas_prestado()

    print("\n--- Realizando devoluciones ---")
    biblioteca.devolver_item(1) # Devolver el préstamo con ID 1 (Juan Pérez, Cien Años de Soledad)
    biblioteca.devolver_item(3) # Devolver el préstamo con ID 3 (Carlos Ruiz, National Geographic)
    biblioteca.devolver_item(1)