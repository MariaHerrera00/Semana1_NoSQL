# A4. Registro del entorno y exploración de un documento

> Este registro no contiene contraseñas. La contraseña de la cuenta de práctica solo se escribe en el prompt de mongosh o en el campo protegido de Compass.

## 1. Sistema y versiones

| Elemento | Versión / dato | Cómo lo verifiqué |
|------------------------|------------------------------------|----------------------------------------|
| Sistema operativo | Windows | Equipo personal |
| Python | 3.14.6 | `python --version` |
| Git | 2.51.0.windows.1 | `git --version` |
| mongosh | 2.13.0 | `mongosh --version` |
| Servidor MongoDB Community | 9.0.2 (local, instalado como servicio de Windows) | Dentro de mongosh: `db.version()` |
| MongoDB Compass | No instalado | La verificación la hice en mongosh, como permite la guía |
| Base de datos | `emprendimiento_sena_lab` | `db.getName()` |
| Usuario de práctica | `aprendiz_nosql` (sin contraseña en este registro) | Lo creé yo con rol `readWrite` solo sobre `emprendimiento_sena_lab` (ver sección 1.1) |
| Base de autenticación | `emprendimiento_sena_lab` | Datos de la cuenta |

Si el instructor entrega otro nombre de base o de usuario, lo cambio aquí y en todos los comandos.

### 1.1 Instalación y cuenta de práctica

Como no tenía una instancia preparada, instalé MongoDB en mi computador. Desde PowerShell **como administrador**:

```powershell
winget install MongoDB.Server
winget install MongoDB.Shell
```

Después creé la cuenta de práctica, con permisos solo de lectura y escritura sobre la base del laboratorio (no es una cuenta administrativa). La contraseña se pide con `passwordPrompt()`, así que no queda escrita en el comando ni en el historial:

```javascript
use emprendimiento_sena_lab
db.createUser({ user: "aprendiz_nosql", pwd: passwordPrompt(), roles: [ { role: "readWrite", db: "emprendimiento_sena_lab" } ] })
```

Resultado: `{ ok: 1 }`.

## 2. Conexión autenticada

En PowerShell el comando va en una sola línea (en Windows no se usa `\` para partir líneas):

```powershell
mongosh "mongodb://127.0.0.1:27017/emprendimiento_sena_lab" --username aprendiz_nosql --authenticationDatabase emprendimiento_sena_lab
```

La contraseña la escribo cuando mongosh la pide (no se ve mientras se escribe). Dentro de mongosh:

```javascript
db = db.getSiblingDB("emprendimiento_sena_lab");
db.runCommand({ping: 1});
db.getName();
```

**Resultado esperado:** `{ ok: 1 }` y `emprendimiento_sena_lab`.
**Resultado obtenido:**

```
emprendimiento_sena_lab> db.runCommand({ping: 1});
{ ok: 1 }
emprendimiento_sena_lab> db.getName();
emprendimiento_sena_lab
```

Al conectar, el servidor mostró esta advertencia: *"Access control is not enabled for the database"*. Significa que en mi instalación local el control de acceso no está activado: me conecté autenticada con `aprendiz_nosql`, pero el servidor también aceptaría conexiones sin usuario. Para esta práctica local no afecta los resultados, pero en un entorno real (como el que prepara el instructor) la autenticación debe estar obligatoria. Activarla implica crear primero un usuario administrador y habilitar `security.authorization` en el archivo `mongod.cfg`; lo dejo como mejora pendiente y no desactivé ni cambié nada de seguridad para "arreglar" la advertencia.

El `ping` solo demuestra que hay conexión; el permiso de lectura y escritura lo compruebo con el script de exploración.

## 3. Exploración del documento (`scripts/01_explorar.js`)

```powershell
mongosh "mongodb://127.0.0.1:27017/emprendimiento_sena_lab" --username aprendiz_nosql --authenticationDatabase emprendimiento_sena_lab --file scripts/01_explorar.js
```

**Resultado esperado:** se muestra el documento `ASE-DEMO-001`, el conteo da `1` y la comprobación de fecha da `true`. Si lo ejecuto otra vez, el conteo sigue en `1` porque el script revisa antes de insertar.
**Resultado obtenido** (también guardado en `evidencias/02_explorar_resultado.txt`):

```
{
  _id: 'ASE-DEMO-001',
  emprendedor_alias: 'Emprendedor ficticio 01',
  iniciativa: { codigo: 'INI-DEMO-001', nombre: 'EcoEmpaque', sector: 'economia_circular' },
  temas: [ 'propuesta de valor', 'validacion de clientes' ],
  modalidad: 'virtual',
  estado: 'programada',
  requiere_seguimiento: true,
  fecha_programada: ISODate('2026-10-08T13:00:00.000Z'),
  fecha_realizacion: null
}
1
true
```

Coincide con lo esperado. Un detalle que noté: mongosh muestra la fecha como `ISODate(...)`, que es la forma en que presenta un valor de tipo Date, y la comprobación `instanceof Date` dio `true`.

### Tipos del documento

| Campo | Valor de ejemplo | Tipo | Explicación |
|------------------|------------------------|--------------|--------------------------------------------|
| `_id` | `"ASE-DEMO-001"` | Cadena (string) | Identificador único dentro de la colección. Es una cadena estable, no un ObjectId; no es contraseña ni da permisos. |
| `emprendedor_alias` | `"Emprendedor ficticio 01"` | Cadena | Alias ficticio, sin datos personales reales. |
| `iniciativa` | `{ codigo, nombre, sector }` | **Subdocumento** | Objeto dentro del documento con los datos básicos de la iniciativa atendida. |
| `iniciativa.sector` | `"economia_circular"` | Cadena | Uno de los sectores del ejercicio. |
| `temas` | `["propuesta de valor", "validacion de clientes"]` | **Arreglo** | Lista corta y acotada de temas tratados. |
| `modalidad` | `"virtual"` | Cadena | Nada en el documento obliga a que sea `virtual` o `presencial`; eso es una regla que hay que validar aparte. |
| `estado` | `"programada"` | Cadena | Estado de la asesoría. |
| `requiere_seguimiento` | `true` | **Booleano** | Es `true` sin comillas. No es lo mismo que la cadena `"true"`. |
| `fecha_programada` | `new Date("2026-10-08T13:00:00Z")` | **Date** | Instante en UTC; en Colombia corresponde a las 08:00 del 8 de octubre. Se comprueba con `instanceof Date` → `true`. |
| `fecha_realizacion` | `null` | Nulo | Nulo explícito: según nuestra regla R6, significa que la asesoría todavía no se ha realizado. |

## 4. Compass

Configuré la conexión con host `127.0.0.1`, puerto `27017`, usuario `aprendiz_nosql`, base de autenticación `emprendimiento_sena_lab` y la contraseña en su campo protegido. Luego ubiqué `emprendimiento_sena_lab` → `asesorias_demo` → documento `ASE-DEMO-001`.
**Resultado:** no instalé Compass en mi equipo, así que hice la verificación en mongosh (sección 3): localicé la base `emprendimiento_sena_lab`, la colección `asesorias_demo` y el documento `ASE-DEMO-001`. Si lo instalo después (`winget install MongoDB.Compass.Community`), los datos de conexión son los de arriba.

No comparto la URI con la contraseña incluida.

## 5. ¿Por qué esta demostración todavía no es el modelo definitivo?

- La colección `asesorias_demo` es solo para experimentar; en S02 se van a decidir las colecciones reales `emprendedores`, `iniciativas` y `asesorias`.
- El documento **copia** el alias del emprendedor y los datos de la iniciativa dentro de la asesoría. Si la iniciativa cambia de nombre, habría que actualizar todas sus asesorías. Todavía no se ha decidido qué se referencia, qué se embebe y qué se guarda como copia histórica (por ejemplo, el sector para Q06).
- Le falta el **código del asesor**, que es necesario para la regla de franjas (R7).
- No hay **validación**: nada impide escribir una modalidad o un estado que no exista, o dejar la fecha como texto.

## 6. Ejercicio de transferencia (`scripts/02_transferencia.js`)

En una copia del ejemplo cambié `_id` a `ASE-DEMO-002`, la iniciativa a `INI-DEMO-002`, el nombre a `Sabores Locales` y el sector a `alimentos`.

**Predicción antes de ejecutar:** se inserta un documento nuevo; el conteo de `ASE-DEMO-002` da `1` y el de `ASE-DEMO-001` sigue en `1`; la fecha sigue siendo `Date` (`true`). Si lo ejecuto dos veces, no se duplica.

**Qué cambia y qué se conserva:** cambian los **valores** de `_id`, `iniciativa.codigo`, `iniciativa.nombre` e `iniciativa.sector`, pero todos siguen siendo cadenas. Los demás campos se conservan igual y con el mismo tipo: `temas` sigue siendo arreglo, `requiere_seguimiento` booleano, `fecha_programada` Date y `fecha_realizacion` null.

**Resultado obtenido** (también en `evidencias/03_transferencia_resultado.txt`):

```
{
  _id: 'ASE-DEMO-002',
  emprendedor_alias: 'Emprendedor ficticio 01',
  iniciativa: { codigo: 'INI-DEMO-002', nombre: 'Sabores Locales', sector: 'alimentos' },
  temas: [ 'propuesta de valor', 'validacion de clientes' ],
  modalidad: 'virtual',
  estado: 'programada',
  requiere_seguimiento: true,
  fecha_programada: ISODate('2026-10-08T13:00:00.000Z'),
  fecha_realizacion: null
}
Conteo ASE-DEMO-001: 1
Conteo ASE-DEMO-002: 1
fecha_programada es Date: true
tipo de iniciativa.sector: string
temas es arreglo: true
requiere_seguimiento es booleano: true
```

La predicción se cumplió: cada ID tiene un solo documento y todos los campos conservaron su tipo.

## 7. Reto de la sección 5.5

- **Atributo específico para una iniciativa de alimentos:** `canal_venta: ["tienda de barrio", "domicilios"]` (arreglo de cadenas), porque una misma iniciativa puede vender por varios canales.
- **Atributo específico para una iniciativa de software:** `modalidad_entrega: "aplicacion_web"` (cadena), para indicar cómo se entrega el servicio digital.
- **Regla que el objeto por sí solo no impone:** que `modalidad` pertenezca al conjunto acordado (`virtual`, `presencial`). Otra: que si `estado` es `realizada`, `fecha_realizacion` no puede ser `null`.

## 8. Dificultad encontrada y cómo la resolví

**1. Error 1603 al instalar el servidor.** La primera vez corrí `winget install MongoDB.Server` desde la terminal de VS Code; descargó todo pero terminó con *"Error del instalador con el código de salida: 1603"*. Ese código indica que el instalador no tenía permisos suficientes, porque MongoDB se instala como servicio de Windows. Lo solucioné abriendo PowerShell con **"Ejecutar como administrador"** y repitiendo el comando: *"Instalado correctamente"*.

**2. `mongosh` no se reconocía.** Después de instalarlo, la terminal decía *"El término 'mongosh' no se reconoce como nombre de un cmdlet…"*. El programa sí estaba instalado, pero la terminal todavía tenía la lista de rutas (PATH) anterior. Lo resolví recargando el PATH en la sesión:

```powershell
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
```

Después, `mongosh --version` mostró `2.13.0`.

**3. Comandos en varias líneas.** En la guía la conexión aparece partida en varias líneas con `\`, pero eso es sintaxis de Linux/macOS. En PowerShell lo escribí en una sola línea.
