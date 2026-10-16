import sqlite3

conexion = sqlite3.connect(":memory:")
conexion.executescript("""
CREATE TABLE emprendedores(id INTEGER PRIMARY KEY, alias TEXT);
CREATE TABLE iniciativas(
    id INTEGER PRIMARY KEY, emprendedor_id INTEGER, estado TEXT
);
INSERT INTO emprendedores VALUES
(1, 'Emprendedor A'), (2, 'Emprendedor B'), (3, 'Emprendedor C');
INSERT INTO iniciativas VALUES
(101, 1, 'activa'), (102, 2, 'archivada'), (103, 1, 'activa');
""")

# Relaciono las tablas con un JOIN: iniciativas.emprendedor_id apunta a emprendedores.id
consulta = """
SELECT i.id, e.alias
FROM iniciativas AS i
INNER JOIN emprendedores AS e ON i.emprendedor_id = e.id
WHERE i.estado = 'activa'
ORDER BY i.id;
"""

if consulta:
    print(conexion.execute(consulta).fetchall())

conexion.close()
