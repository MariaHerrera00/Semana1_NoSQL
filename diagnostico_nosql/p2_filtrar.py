iniciativas = [
    {"codigo": "INI-001", "sector": "tecnologia", "pendiente": True},
    {"codigo": "INI-002", "sector": "alimentos", "pendiente": True},
    {"codigo": "INI-003", "sector": "tecnologia", "pendiente": False},
    {"codigo": "INI-004", "sector": "tecnologia"}
]

def seleccionar_pendientes(registros, sector):
    # Retorna códigos del sector indicado con pendiente exactamente True.
    # No modifica la lista recibida: solo la recorre y arma una lista nueva.
    # Si falta el campo "pendiente", la iniciativa NO se selecciona: no se puede
    # asumir que está pendiente si no hay un dato que lo diga (.get devuelve None).
    codigos = []
    for registro in registros:
        if registro.get("sector") == sector and registro.get("pendiente") is True:
            codigos.append(registro["codigo"])
    return codigos


# Prueba 1: con resultados
resultado = seleccionar_pendientes(iniciativas, "tecnologia")
print("Pendientes de tecnologia:", resultado)
assert resultado == ["INI-001"]

# Prueba 2: sin resultados (no hay iniciativas de ese sector)
resultado = seleccionar_pendientes(iniciativas, "economia_circular")
print("Pendientes de economia_circular:", resultado)
assert resultado == []

# Compruebo que la lista original no cambió
assert len(iniciativas) == 4 and "pendiente" not in iniciativas[3]

# Por qué no confundir cadena con booleano: si un registro tuviera "pendiente": "False",
# esa cadena NO es el booleano False. Con "is True" solo se acepta el booleano True,
# así un texto como "True" o "False" no se cuela por error.
prueba_cadena = [{"codigo": "INI-005", "sector": "alimentos", "pendiente": "True"}]
print("Con pendiente como texto:", seleccionar_pendientes(prueba_cadena, "alimentos"))
assert seleccionar_pendientes(prueba_cadena, "alimentos") == []

print("Todas las pruebas pasaron")
