// 01_explorar.js - Semana 1 Bases de Datos NoSQL
// Inserta (si no existe) una asesoría demostrativa, la localiza y comprueba el tipo de la fecha.
// Se ejecuta con una sesión autenticada (cuenta aprendiz_nosql), nunca con la cuenta administrativa.

db = db.getSiblingDB("emprendimiento_sena_lab");

if (db.asesorias_demo.countDocuments({_id: "ASE-DEMO-001"}) === 0) {
  db.asesorias_demo.insertOne({
    _id: "ASE-DEMO-001",
    emprendedor_alias: "Emprendedor ficticio 01",
    iniciativa: {
      codigo: "INI-DEMO-001",
      nombre: "EcoEmpaque",
      sector: "economia_circular"
    },
    temas: ["propuesta de valor", "validacion de clientes"],
    modalidad: "virtual",
    estado: "programada",
    requiere_seguimiento: true,
    fecha_programada: new Date("2026-10-08T13:00:00Z"),
    fecha_realizacion: null
  });
}

printjson(db.asesorias_demo.findOne({_id: "ASE-DEMO-001"}));
print(db.asesorias_demo.countDocuments({_id: "ASE-DEMO-001"}));

const asesoria = db.asesorias_demo.findOne({_id: "ASE-DEMO-001"});
print(asesoria.fecha_programada instanceof Date);
