import json

# Versión original (la dejo tal cual para no ocultar el intento fallido)
texto = '{"codigo":"INI-001", "activa":True, "intereses":["Validar mercado",]}'

# 1. Intento cargar el texto con json.loads
try:
    datos = json.loads(texto)
except json.JSONDecodeError as error:
    # 2. Registro el error
    print("Error al cargar el texto original:", error)

# 2. Corrijo la sintaxis sin cambiar la intención:
#    - True (Python) -> true (JSON, en minúscula)
#    - Quito la coma que sobra después de "Validar mercado"
texto_corregido = '{"codigo":"INI-001", "activa":true, "intereses":["Validar mercado"]}'

datos = json.loads(texto_corregido)

# 3. Muestro codigo y activa con sus tipos
print("codigo:", datos["codigo"], "-> tipo:", type(datos["codigo"]).__name__)
print("activa:", datos["activa"], "-> tipo:", type(datos["activa"]).__name__)

# 4. Explicación de las correcciones
#    En JSON los booleanos se escriben true / false en minúscula. True con mayúscula
#    es la forma de Python, por eso json.loads no lo reconoce y dice "Expecting value".
#    Al corregirlo aparece un segundo error: JSON no permite una coma al final de una
#    lista ("trailing comma"), así que la quité. La intención se conserva: la iniciativa
#    INI-001 está activa y tiene un interés, "Validar mercado".
#    Al cargarlo, true se convierte en True de Python (tipo bool) y el código queda como str.
