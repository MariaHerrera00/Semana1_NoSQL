# A2. Comparación de necesidades y familias NoSQL

Para cada caso pensé primero en **cómo se va a consultar la información** y después en el modelo. Como dice la guía, no se trata de escoger la tecnología de moda sino la que encaja con lo que se consulta junto, lo que cambia junto y cuánto crece.

## Matriz de selección

| Caso | Modelo propuesto | Razón vinculada a una consulta | Límite o costo | Alternativa |
|----------------|-------------|-------------------------|--------------------------|--------------------|
| **Iniciativas de varios sectores** | Documental (MongoDB) | Para la consulta "ver el detalle de una iniciativa con su propuesta de valor y sus atributos específicos" (Q02) puedo traer todo en un solo documento: los campos comunes (código, nombre, sector, etapa, estado) más un subdocumento con lo propio del sector, sin tener que crear columnas vacías para los demás sectores. | La flexibilidad no es gratis: si no defino un contrato para los campos comunes, cada quien puede escribir los campos distinto (`sector: "Tecnología"` vs `"tecnologia"`). Habría que agregar validación. Además, cruzar con emprendedores o asesorías ($lookup) es más costoso que un JOIN bien indexado. | SQL: una tabla `iniciativas` con los campos comunes y tablas por sector, o una columna JSON (por ejemplo JSONB en PostgreSQL) para los atributos específicos. |
| **Sesiones temporales de un portal** | Clave-valor (Redis) | La consulta es siempre la misma: "dado el token de la sesión, ¿quién es el usuario y sigue vigente?". Es un acceso por clave exacta, muy rápido, y con un tiempo de expiración (TTL) la sesión se borra sola cuando vence. | Solo puedo buscar por la clave; no sirve para preguntas como "¿cuántas sesiones abrió un usuario este mes?". Los datos viven en memoria, así que si el servidor se reinicia sin persistencia se pierden (para sesiones es aceptable, para un historial no). Es un motor más que mantener. | Tabla `sesiones` en SQL con `fecha_expiracion` y una tarea que limpie las vencidas, o una colección en MongoDB con índice TTL. |
| **Recorridos entre emprendedores, mentores y habilidades** | Grafos (Neo4j) | Una consulta como "¿qué mentores tienen la habilidad *marketing digital* y ya asesoraron a emprendedores conectados con este emprendedor?" es recorrer varias relaciones seguidas. En un grafo las relaciones son parte del dato y se recorren directamente, sin encadenar muchos JOIN. | Hay que aprender otro lenguaje (Cypher) y operar otro motor. Para reportes de conteos masivos no es lo más práctico, y si las relaciones son pocas y de un solo salto, un grafo es exagerado. | SQL con tablas intermedias (`mentor_habilidad`, `asesoria`) y consultas recursivas (`WITH RECURSIVE`) cuando los saltos son pocos. |
| **Lecturas de sensores por dispositivo y periodo (agroindustria a gran escala)** | Familias de columnas (Cassandra) | La consulta prevista es "todas las lecturas del sensor S en el día D, ordenadas por hora". Puedo definir la partición por (dispositivo, día) y ordenar dentro de ella por fecha y hora, así cada consulta lee una sola partición aunque lleguen millones de lecturas. | Hay que diseñar una tabla por cada consulta: si después piden algo no previsto (por ejemplo "todas las lecturas mayores a 40 °C de cualquier sensor"), es muy difícil. No hay JOIN y montar un clúster es complejo para un proyecto pequeño. | Una base de series de tiempo (por ejemplo TimescaleDB) o una colección *time series* de MongoDB si el volumen no es tan grande. |

## Una situación en la que conservaría SQL

El registro de **asistencia de aprendices a talleres de la Unidad**, donde cada registro tiene siempre los mismos campos (aprendiz, taller, fecha, asistió), hay muchas relaciones fijas (aprendiz–ficha–taller) y se necesitan reportes con JOIN y totales exactos. Ahí la estructura no varía, la integridad referencial es importante y SQL resuelve bien todo eso. Es parecido a lo que hice en el sistema de Gestión de Aprendices con PHP y MySQL: los datos eran muy regulares y las tablas relacionadas funcionaban perfecto.

## Práctica de la sección 5.1

**Dos razones para evaluar documentos en el caso de la Unidad de Emprendimiento:**

1. Las iniciativas tienen atributos distintos según el sector (una de alimentos tiene producto y canal de venta; una de software, servicio digital y forma de entrega). En documentos cada iniciativa guarda solo lo que le aplica, sin columnas vacías.
2. Varias consultas piden ver la información junta (el detalle de una iniciativa, o una asesoría con los datos básicos de la iniciativa atendida). Un documento puede traer esa información en una sola lectura.

**Una razón para preferir SQL bajo otros requisitos:** si la Unidad necesitara operaciones que deben cumplirse todas o ninguna sobre varias tablas a la vez (por ejemplo, manejo de recursos o convocatorias con montos) y reportes muy cruzados entre muchas entidades, la integridad referencial y las transacciones de SQL serían más seguras y sencillas de mantener.

> La flexibilidad no elimina la necesidad de modelar: aunque MongoDB no me obligue a tener un esquema, yo sí tengo que decidir qué campos son comunes, cuáles son obligatorios y qué valores son válidos.
