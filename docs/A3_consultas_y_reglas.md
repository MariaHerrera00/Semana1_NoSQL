# A3. Reglas y consultas de la Unidad de Emprendimiento

Antes de pensar en colecciones o comandos, escribí las seis consultas en lenguaje natural y definí qué entra y qué sale de cada una. Las frecuencias son **hipótesis** mías sobre cómo se usaría el sistema, no estadísticas medidas.

## Consultas Q01–Q06

| ID | Consulta en lenguaje natural | Actor | Filtros (entrada) | Campos de salida | Orden | Frecuencia estimada (hipótesis) |
|-------|---------------|-----------|---------------------|------------------|---------------|-------------|
| **Q01** | Mostrar las iniciativas activas de un sector y una etapa didáctica. | Responsable de la unidad / asesor | `estado = "activa"`, `sector` (ej. `tecnologia`), `etapa` (ej. `validacion`). Sector y etapa son opcionales: si no se envían, se muestran todas las activas. | código, nombre, sector, etapa, código y alias del emprendedor responsable | sector, luego etapa (idea → validacion → puesta_en_marcha), luego nombre A-Z | Varias veces al día |
| **Q02** | Ver el detalle completo de una iniciativa, con su propuesta de valor y sus atributos específicos del sector. | Asesor (antes de una asesoría) | `codigo` de la iniciativa (ej. `INI-001`) | todos los campos comunes, `propuesta_valor`, atributos específicos del sector, código y alias del responsable, estado | No aplica (devuelve una sola iniciativa) | Alta: cada vez que se prepara una asesoría |
| **Q03** | Listar las iniciativas de un emprendedor responsable, filtrando por estado. | Responsable de la unidad | `codigo` del emprendedor (ej. `EMP-003`), `estado` opcional (`activa` / `archivada`) | código, nombre, sector, etapa, estado, fecha de registro | estado (activas primero), luego fecha de registro más reciente | Media: algunas veces por semana |
| **Q04** | Consultar las asesorías programadas pendientes en un rango de fechas y una modalidad. | Asesor / responsable de agenda | `estado = "programada"`, `fecha_programada` desde (incluida) hasta (excluida), `modalidad` (`virtual` / `presencial`). Las fechas del rango se interpretan en hora de Colombia y se guardan en UTC. | código de la asesoría, fecha y hora programada, modalidad, código del asesor, código y nombre de la iniciativa | `fecha_programada` ascendente (la más próxima primero) | Diaria (al iniciar la jornada) |
| **Q05** | Ver el historial de asesorías de una iniciativa. | Asesor / responsable de la unidad | `codigo` de la iniciativa. Incluye todas las asesorías (programadas, realizadas y canceladas) aunque la iniciativa esté archivada. | código de la asesoría, estado, fecha programada, fecha de realización, temas, modalidad, código del asesor | `fecha_programada` ascendente (orden cronológico) | Media: antes de cada asesoría de seguimiento |
| **Q06** | Contar cuántas asesorías se realizaron por sector de la iniciativa y por mes. | Responsable de la unidad (reporte) | `estado = "realizada"`, año (ej. 2026). El mes se calcula con `fecha_realizacion` en hora de Colombia. | sector, mes (AAAA-MM), cantidad de asesorías | mes ascendente, luego sector | Mensual (informe de gestión) |

### Decisión sobre el sector en Q06

Decidí que en Q06 el sector debe ser **el que tenía la iniciativa al momento de la asesoría**, no el valor actual. Si una iniciativa empezó en `alimentos` y después se reclasifica como `economia_circular`, las asesorías que ya se hicieron deben seguir contando para `alimentos`; si no, el informe de un mes que ya pasó cambiaría cada vez que alguien edita una iniciativa. Esto implica que, al modelar en S02, la asesoría probablemente debe guardar una copia (snapshot) del sector. Lo dejo planteado para retomarlo en la semana 2.

## Reglas del caso

| # | Regla | ¿La ajusto? Justificación |
|------|---------------------------------------------|-------------------------------------------------|
| R1 | Los códigos de emprendedores, iniciativas y asesorías son únicos. Formato del ejercicio: `EMP-001`, `INI-001`, `ASE-001`. | Sin ajuste. Agrego el formato para que sea fácil reconocer a qué entidad pertenece un código. |
| R2 | Cada iniciativa tiene **un** emprendedor responsable que debe existir. Una persona puede ser responsable de varias iniciativas. | Sin ajuste. Los equipos de varios socios quedan para una versión posterior, como dice la guía. |
| R3 | Cada asesoría se vincula con una iniciativa existente y registra el código ficticio del asesor (ej. `ASR-01`). | Sin ajuste. El asesor se identifica solo por código, sin datos de contacto. |
| R4 | Sectores válidos: `tecnologia`, `alimentos`, `economia_circular`. Etapas didácticas: `idea`, `validacion`, `puesta_en_marcha`. | Ajuste: se escriben siempre en minúscula, sin tildes y con guion bajo, para que `"Tecnología"` y `"tecnologia"` no cuenten como sectores distintos. No son categorías oficiales del SENA. |
| R5 | Estado de iniciativa: `activa` o `archivada`. Estado de asesoría: `programada`, `realizada` o `cancelada`. | Sin ajuste. |
| R6 | Toda asesoría tiene `fecha_programada`. Cuando se realiza, se registra `fecha_realizacion`, que puede ser distinta de la programada. La fecha programada no se modifica para ocultar una reprogramación. | Ajuste: mientras la asesoría está `programada` o `cancelada`, `fecha_realizacion` es `null` (no se deja ausente ni como cadena vacía); si está `realizada`, `fecha_realizacion` es obligatoria y de tipo fecha. |
| R7 | No se programan dos asesorías del mismo asesor en la misma franja. | Ajuste: defino la **franja del laboratorio** como bloques de 1 hora que empiezan en punto (08:00–09:00, 09:00–10:00, … en hora de Colombia). Una asesoría ocupa la franja en la que empieza su `fecha_programada`. Las asesorías `canceladas` no ocupan franja, para que se pueda volver a usar ese espacio. |
| R8 | Archivar una iniciativa no elimina su historial de asesorías. | Sin ajuste. Archivar es un cambio de estado, no un borrado; el historial (Q05) se sigue pudiendo consultar. |

### Reglas funcionales vs. mecanismos

Las reglas de arriba dicen **qué** debe cumplirse y se pueden explicar sin una pantalla ni un motor concreto. El **cómo** garantizarlas es lo que vamos a aprender más adelante:

| Regla funcional | Posible mecanismo (a estudiar después) |
|----------------------------------------|------------------------------------------------------------|
| Códigos únicos (R1) | Usar el código como `_id` o un índice único |
| Responsable / iniciativa existentes (R2, R3) | Validación en la aplicación antes de insertar; MongoDB no tiene claves foráneas como SQL |
| Valores permitidos de sector, etapa, estado, modalidad (R4, R5) | Validación de esquema (`$jsonSchema`) con listas de valores (`enum`) |
| Coherencia de fechas según estado (R6) | Validación de esquema y reglas en la aplicación |
| Un asesor no puede tener dos asesorías en la misma franja (R7) | Índice único compuesto (asesor + franja) para asesorías no canceladas. Comprobar antes de insertar **no basta** si dos personas programan al mismo tiempo; esa garantía concurrente se verá más adelante. |
| Archivar no borra el historial (R8) | Cambiar el campo `estado` en lugar de usar `deleteOne` / `deleteMany` |

## Dos preguntas para la persona responsable de la unidad

1. ¿Una asesoría puede atender **a varias iniciativas a la vez** (por ejemplo, un taller grupal), o siempre es una iniciativa por asesoría? Esto cambia si la asesoría guarda una iniciativa o una lista.
2. Cuando una asesoría se **reprograma**, ¿prefieren cancelarla y crear una nueva, o cambiar la fecha guardando un historial de cambios? Y ¿cuánto dura normalmente una asesoría? Necesito saberlo para confirmar si la franja de 1 hora es correcta.

## Riesgo identificado

**Doble reserva de un asesor:** si dos personas programan al mismo asesor en la misma franja casi al mismo tiempo, las dos pueden ver la franja libre y guardar la asesoría, quedando el asesor con dos citas cruzadas. Revisar antes de insertar no evita este caso. Mientras se aprende el mecanismo adecuado, la mitigación es que una sola persona maneje la agenda de cada asesor y que exista un reporte que detecte franjas duplicadas.

También veo un riesgo de **calidad de datos**: si los sectores, etapas o modalidades se escriben a mano sin validación, los reportes como Q06 pueden salir mal (sectores repetidos con distinta escritura).
