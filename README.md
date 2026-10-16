# Bases de Datos NoSQL – Semana 1 (E01)

**Aprendiz:** María Paula Herrera Rivas
**Programa:** Tecnología en Análisis y Desarrollo de Software (ADSO) – SENA CTMA
**Instructor:** Wilson Castro Gil
**Caso integrador:** Unidad de Emprendimiento del SENA (datos y reglas ficticios de laboratorio)

## ¿Qué hay en este repositorio?

```
bases-nosql-semana1/
├── docs/
│   ├── A2_matriz_modelos.md      # comparación de familias NoSQL y cuándo conservar SQL
│   ├── A3_consultas_y_reglas.md  # Q01–Q06, reglas del caso, preguntas y riesgo
│   ├── entorno.md                # registro del entorno, tipos del documento y transferencia
│   └── A5_socializacion.md       # presentación y acción de mejora
├── scripts/
│   ├── 00_fechas.js              # ejemplo de fechas (5.4), corre sin servidor
│   ├── 01_explorar.js            # laboratorio guiado (5.7)
│   └── 02_transferencia.js       # ejercicio de transferencia: ASE-DEMO-002
├── evidencias/                   # resultados y capturas SIN contraseñas
├── diagnostico_nosql/            # DGN-01: respuestas, p1_json.py, p2_filtrar.py, p3_sql.py
├── .gitignore
└── README.md
```

El diagnóstico individual (DGN-01) está en `diagnostico_nosql/`. Como trabajé sola, lo incluí en el mismo repositorio; no contiene datos sensibles. Sus ejercicios se ejecutan con Python 3 (solo biblioteca estándar):

```powershell
python diagnostico_nosql/p1_json.py
python diagnostico_nosql/p2_filtrar.py
python diagnostico_nosql/p3_sql.py
```

## Requisitos

- `mongosh` instalado (`mongosh --version`).
- MongoDB con la cuenta de práctica `aprendiz_nosql` sobre la base `emprendimiento_sena_lab`. Yo lo instalé localmente (MongoDB Community 9.0.2 con `winget install MongoDB.Server`, y mongosh 2.13.0 con `winget install MongoDB.Shell`, desde PowerShell como administrador). Los pasos para crear la cuenta están en `docs/entorno.md`.
- Opcional: MongoDB Compass.

## Cómo ejecutar

Desde la carpeta del repositorio (en PowerShell, cada comando en una sola línea):

```powershell
# 1. Ejemplo de fechas, no necesita servidor
mongosh --nodb --file scripts/00_fechas.js

# 2. Laboratorio guiado: pide la contraseña en el prompt
mongosh "mongodb://127.0.0.1:27017/emprendimiento_sena_lab" --username aprendiz_nosql --authenticationDatabase emprendimiento_sena_lab --file scripts/01_explorar.js

# 3. Transferencia
mongosh "mongodb://127.0.0.1:27017/emprendimiento_sena_lab" --username aprendiz_nosql --authenticationDatabase emprendimiento_sena_lab --file scripts/02_transferencia.js
```

En Linux o macOS el comando se puede partir en varias líneas con `\`.

### Resultados esperados

| Script | Resultado |
|---|---|
| `00_fechas.js` | `string` y `true` |
| `01_explorar.js` | documento `ASE-DEMO-001`, conteo `1`, `true` |
| `02_transferencia.js` | documento `ASE-DEMO-002`, ambos conteos en `1`, la fecha sigue siendo Date |

Los scripts se pueden ejecutar varias veces: revisan si el documento existe antes de insertarlo, así que no se duplica. Esa revisión **no** es una solución para inserciones simultáneas; eso se estudia más adelante.

## Seguridad

- Nunca escribo la contraseña en los comandos, en los scripts ni en este repositorio.
- No uso la cuenta administrativa.
- El `.gitignore` excluye `.env`, `secrets/`, `.venv/`, `__pycache__/` y `*.log`. Antes de cada commit reviso `git status --short`.
- Si una credencial llegara a subirse por error, no basta con borrarla o ignorarla después: hay que avisar al responsable para cambiarla (rotarla) y limpiar el historial.
- Todos los datos son ficticios: alias y códigos, sin documentos de identidad ni contactos reales.
