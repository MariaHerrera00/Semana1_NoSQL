// 00_fechas.js - Ejemplo de la sección 5.4 (se puede correr sin servidor: mongosh --nodb --file scripts/00_fechas.js)
const fechaTexto = "2026-10-06T13:00:00Z";
const fechaDato = new Date(fechaTexto);

print(typeof fechaTexto);          // string
print(fechaDato instanceof Date);  // true
