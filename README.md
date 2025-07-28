# Prueba-EmasT
## Para probar los códigos alamacenados en este repositorio deberás descargar el contenido del repositorio a tu máquina local 

## Parte 1

Para la primera parte de la prueba técnica de inmersión tendremos los archivos nombrados `fibonacci.py` , `palíndromo.py`, `anagrama.py` y `fizzbuzz.py` los cuales deberás ejecutar con uno de los siguientes comandos: `python3 (nombre del código)` ó `python (nombre del código)`

La versión que uses depende que versión de python usa tu máquina local

### `fibonacci.py`
<img width="1085" height="118" alt="image" src="https://github.com/user-attachments/assets/f6762035-47ae-4f2c-a887-3694fce3b465" />

### `palíndromo.py`
<img width="921" height="164" alt="image" src="https://github.com/user-attachments/assets/661459e7-4fa2-49d9-95bc-1a429f0eb5bc" />

### `anagrama.py`
<img width="921" height="234" alt="image" src="https://github.com/user-attachments/assets/dc183a51-2776-4469-b616-80d502c0c1cf" />

### `fizzbuzz.py`
<img width="921" height="700" alt="image" src="https://github.com/user-attachments/assets/bc0ebf8a-5e47-41d7-8b1b-a712ed56b0ca" />

## Parte 2

Para la segunda parte de la prueba técnica de inmersión tendremos la carpeta llamada POO, la cual contiene un archivo llamado `app.py` en la que está contenido todo lo solicitado en el entregable y para ejecutarla se deben ejecutar uno de los sguientes comandos: `python3 app.py` ó `python app.py`
Este proyecto implementa una aplicación sencilla  utilizando los principios de la Programación Orientada a Objetos (POO) en Python y persistencia de datos a través de una base de datos relacional SQLite. La aplicación permite agregar libros  y revistas manualmente dentro del código fuente, realizar préstamos y devoluciones, y consultar el estado de los ítems.
Tenemos las clases bases que son `Item`, `Libro` y `Revista` donde las dos últimas heredan de la primera, además tenemos la clase `Biblioteca` que gestiona la colección de ítems y las interacciones con la base de datos, a los ítems se accede a través de propiedades (`@property`), garantizando la encapsulación. También, se hizo uso de un método polimórfico `mostrar_info()` en la clase base `Item`, el cual es sobrescrito en las clases derivadas `Libro` y `Revista` para mostrar información específica de cada tipo de ítem.

Al ejecutar la aplicación visibilizamos lo siguiente:

<img width="1005" height="800" alt="image" src="https://github.com/user-attachments/assets/baf0a7a6-880b-497b-a74a-d1107a5f1776" />
<img width="1497" height="903" alt="image" src="https://github.com/user-attachments/assets/551253e4-fe55-4f18-8ecb-7cebfc19f63b" />

### Esquema de la base de datos
<img width="650" height="567" alt="image" src="https://github.com/user-attachments/assets/9621357d-ef36-47dd-8b3d-ec40e13c3a43" />

### Consultas SQL solicitadas
Listar todos los ítems disponibles

```sql
SELECT id, tipo, titulo, autor_editor, cantidad_disponible
FROM items
WHERE cantidad_disponible > 0;
```

Listar los ítems prestados actualmente

```sql
SELECT p.id, i.titulo, i.tipo, p.prestatario, p.fecha_prestamo, p.fecha_devolucion_esperada
FROM prestamos p
JOIN items i ON p.item_id = i.id
WHERE p.fecha_devolucion_real IS NULL;
```

Calcular el ítem más prestado

```sql
SELECT i.titulo, i.tipo, COUNT(p.item_id) AS total_prestamos
FROM prestamos p
JOIN items i ON p.item_id = i.id
GROUP BY p.item_id
ORDER BY total_prestamos DESC
LIMIT 1;
```

## Parte 3

#### Diagrama de clases UML

<img width="1110" height="723" alt="image" src="https://github.com/user-attachments/assets/9c4d3995-b289-47e9-89f5-e84d7643af6d" />

#### Descripción de funcionalidad
La funcionalidad de "agregar al carrito" implica los siguientes pasos y lógica:
- Identificación del Usuario y Carrito: Cuando un usuario (autenticado o invitado) desea agregar un producto, el sistema primero identifica si el usuario ya tiene un carrito de compras activo.
- Selección del Producto y Cantidad: El usuario selecciona un Producto específico y la cantidad deseada.
- Verificación de Stock: Antes de agregar, el sistema verifica si la cantidad solicitada está disponible en el stock del Producto. Si no hay suficiente stock, se notifica al usuario.
- Actualización del Carrito
- Actualización de la Interfaz de Usuario: La interfaz de usuario se actualiza para reflejar el nuevo contenido del carrito (ej. un contador de ítems en el icono del carrito).

#### Esquema base de datos
Tabla usuarios

```sql
CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_usuario TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    contrasena_hash TEXT NOT NULL,
    direccion TEXT,
    telefono TEXT,
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP
);

```

Tabla productos

```sql
CREATE TABLE IF NOT EXISTS productos (
    id_producto INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    descripcion TEXT,
    precio REAL NOT NULL,
    stock INTEGER NOT NULL,
    categoria TEXT,
    url_imagen TEXT
);
```

Tabla carritos

```sql
CREATE TABLE IF NOT EXISTS carritos (
    id_carrito INTEGER PRIMARY KEY AUTOINCREMENT,
    id_usuario INTEGER,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    fecha_ultima_actualizacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    estado TEXT DEFAULT 'activo', -- 'activo', 'comprado', 'abandonado'
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
);
```

Tabla ordenes

```sql
CREATE TABLE IF NOT EXISTS ordenes (
    id_orden INTEGER PRIMARY KEY AUTOINCREMENT,
    id_usuario INTEGER NOT NULL,
    fecha_orden DATETIME DEFAULT CURRENT_TIMESTAMP,
    estado TEXT DEFAULT 'pendiente', -- 'pendiente', 'procesando', 'enviado', 'entregado', 'cancelado'
    total_orden REAL NOT NULL,
    direccion_envio TEXT NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
);

```

Tabla pagos

```sql
CREATE TABLE IF NOT EXISTS pagos (
    id_pago INTEGER PRIMARY KEY AUTOINCREMENT,
    id_orden INTEGER NOT NULL UNIQUE, 
    metodo_pago TEXT NOT NULL,
    monto REAL NOT NULL,
    fecha_pago DATETIME DEFAULT CURRENT_TIMESTAMP,
    estado TEXT DEFAULT 'pendiente', -- 'aprobado', 'rechazado', 'pendiente'
    transaccion_id TEXT,
    FOREIGN KEY (id_orden) REFERENCES ordenes(id_orden)
);
```
