// 02_transferencia.js - Ejercicio de transferencia (sección 5.7)
// (Uso var en "copia" para poder pegar el bloque dos veces en la misma sesión de mongosh sin error de redeclaración.)
// Copia del ejemplo con: ASE-DEMO-002, INI-DEMO-002, "Sabores Locales", sector alimentos.
// Predicción antes de ejecutar:
//   - Se inserta un documento nuevo con _id "ASE-DEMO-002" (la primera vez).
//   - findOne lo muestra; countDocuments por ese ID da 1.
//   - fecha_programada sigue siendo Date -> true.
//   - El conteo de ASE-DEMO-001 sigue en 1 (no se toca).
//   - Si lo ejecuto dos veces seguidas, no se duplica: el conteo sigue en 1.

db = db.getSiblingDB("emprendimiento_sena_lab");

if (db.asesorias_demo.countDocuments({_id: "ASE-DEMO-002"}) === 0) {
  db.asesorias_demo.insertOne({
    _id: "ASE-DEMO-002",
    emprendedor_alias: "Emprendedor ficticio 01",
    iniciativa: {
      codigo: "INI-DEMO-002",
      nombre: "Sabores Locales",
      sector: "alimentos"
    },
    temas: ["propuesta de valor", "validacion de clientes"],
    modalidad: "virtual",
    estado: "programada",
    requiere_seguimiento: true,
    fecha_programada: new Date("2026-10-08T13:00:00Z"),
    fecha_realizacion: null
  });
}

printjson(db.asesorias_demo.findOne({_id: "ASE-DEMO-002"}));

print("Conteo ASE-DEMO-001:", db.asesorias_demo.countDocuments({_id: "ASE-DEMO-001"}));
print("Conteo ASE-DEMO-002:", db.asesorias_demo.countDocuments({_id: "ASE-DEMO-002"}));

var copia = db.asesorias_demo.findOne({_id: "ASE-DEMO-002"});
print("fecha_programada es Date:", copia.fecha_programada instanceof Date);
print("tipo de iniciativa.sector:", typeof copia.iniciativa.sector);
print("temas es arreglo:", Array.isArray(copia.temas));
print("requiere_seguimiento es booleano:", typeof copia.requiere_seguimiento === "boolean");
