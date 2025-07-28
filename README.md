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

```python

SELECT id, tipo, titulo, autor_editor, cantidad_disponible
FROM items
WHERE cantidad_disponible > 0;

Listar los ítems prestados actualmente

```python

SELECT p.id, i.titulo, i.tipo, p.prestatario, p.fecha_prestamo, p.fecha_devolucion_esperada
FROM prestamos p
JOIN items i ON p.item_id = i.id
WHERE p.fecha_devolucion_real IS NULL;

Calcular el ítem más prestado

```python

SELECT i.titulo, i.tipo, COUNT(p.item_id) AS total_prestamos
FROM prestamos p
JOIN items i ON p.item_id = i.id
GROUP BY p.item_id
ORDER BY total_prestamos DESC
LIMIT 1;

