# A5. Socialización de E01 y nivelación

## Lo que presento

| Elemento | Mi aporte |
|--------------------|--------------------------------------------------------------------------------|
| **Una elección de modelo** | Para las iniciativas de varios sectores elijo el modelo **documental** (MongoDB), porque la consulta Q02 trae el detalle de una iniciativa con sus atributos específicos en una sola lectura. Su límite es que la flexibilidad exige definir un contrato y validar los campos comunes. |
| **Una consulta** | **Q04:** asesorías `programadas` en un rango de fechas (desde incluido, hasta excluido) y una modalidad, ordenadas por `fecha_programada` de la más próxima a la más lejana. Entrada: rango y modalidad. Salida: código, fecha, modalidad, asesor e iniciativa. |
| **Un tipo** | `fecha_programada` es de tipo **Date**, no texto. `"2026-10-08T13:00:00Z"` entre comillas es una cadena aunque parezca fecha; con `new Date(...)` se vuelve un Date y se comprueba con `instanceof Date`. En Colombia ese instante es a las 08:00. |
| **Una dificultad** | Diferenciar **campo ausente, `null` y cadena vacía**. Entendí que `fecha_realizacion: null` puede significar "todavía no se ha realizado" solo si así lo definimos en las reglas (R6), y que no se debe usar `""` para una fecha desconocida. |

## Retroalimentación del compañero (lista E01)

| Compañero(a) | Fortaleza que señaló | Sugerencia de mejora |
|---|---|---|
| Por diligenciar en la socialización | | |

## Acción de mejora acordada

| Acción concreta | Fecha acordada |
|---|---|
| Repasar consultas SQL con JOIN y practicar la diferencia entre `null`, campo ausente y cadena vacía con ejemplos en Python y en mongosh. | Antes de la sesión de la semana 2 (por confirmar con el instructor) |
