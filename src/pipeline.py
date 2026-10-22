import csv
import json
import re
from pathlib import Path

from pasajero import GRUPOS_EDAD, Pasajero

COLUMNAS_REQUERIDAS = ("PassengerId", "Survived", "Pclass", "Name", "Age", "Ticket")

# Billete: hasta dos prefijos opcionales de letras, números, puntos o barras
# (por ejemplo "PC", "A/5", "STON/O 2.") seguidos de un número de 1 a 7 cifras.
# Se acepta además el valor especial "LINE", que aparece sin número.
PATRON_BILLETE = re.compile(r"^(?:[A-Za-z0-9./]+ ){0,2}\d{1,7}$|^LINE$")

EDAD_MAXIMA = 100


def validar_esquema(registros):
    faltantes = [col for col in COLUMNAS_REQUERIDAS if col not in registros[0]]
    if faltantes:
        raise ValueError(f"Faltan columnas obligatorias en los datos: {', '.join(faltantes)}")


def normalizar_campos(registros):
    return [
        {clave.strip(): valor.strip() for clave, valor in fila.items()}
        for fila in registros
    ]


def billete_valido(billete):
    return PATRON_BILLETE.match(billete) is not None


def crear_pasajero(fila):
    try:
        id_pasajero = int(fila["PassengerId"])
    except ValueError:
        raise ValueError(f"PassengerId no es un entero: '{fila['PassengerId']}'")
    if id_pasajero <= 0:
        raise ValueError(f"PassengerId debe ser positivo: {id_pasajero}")

    if fila["Survived"] not in ("0", "1"):
        raise ValueError(f"Survived debe ser 0 o 1: '{fila['Survived']}'")

    if fila["Pclass"] not in ("1", "2", "3"):
        raise ValueError(f"Pclass debe ser 1, 2 o 3: '{fila['Pclass']}'")

    if fila["Name"] == "":
        raise ValueError("Name está vacío")

    if not billete_valido(fila["Ticket"]):
        raise ValueError(f"Ticket con formato inválido: '{fila['Ticket']}'")

    if fila["Age"] == "":
        edad = None
    else:
        try:
            edad = float(fila["Age"])
        except ValueError:
            raise ValueError(f"Age no es un número: '{fila['Age']}'")
        if not 0 < edad <= EDAD_MAXIMA:
            raise ValueError(f"Age fuera de rango (0, {EDAD_MAXIMA}]: {edad}")

    return Pasajero(
        id_pasajero=id_pasajero,
        nombre=fila["Name"],
        billete=fila["Ticket"],
        clase=int(fila["Pclass"]),
        edad=edad,
        sobrevivio=fila["Survived"] == "1",
    )


def limpiar_datos(registros):
    pasajeros = []
    rechazos = []
    ids_vistos = set()
    for numero_fila, fila in enumerate(registros, start=1):
        try:
            pasajero = crear_pasajero(fila)
            if pasajero.id in ids_vistos:
                raise ValueError(f"PassengerId duplicado: {pasajero.id}")
        except ValueError as error:
            rechazos.append({
                "fila": numero_fila,
                "PassengerId": fila.get("PassengerId", ""),
                "motivo": str(error),
            })
            continue
        ids_vistos.add(pasajero.id)
        pasajeros.append(pasajero)
    return pasajeros, rechazos


def indexar_pasajeros(pasajeros):
    return {pasajero.id: pasajero for pasajero in pasajeros}


def buscar_pasajero(indice, id_pasajero):
    return indice.get(id_pasajero)


def filtrar_grupo(pasajeros, clase=None, grupo_edad=None):
    if clase is not None and clase not in (1, 2, 3):
        raise ValueError(f"La clase debe ser 1, 2 o 3, no {clase}")
    if grupo_edad is not None and grupo_edad not in GRUPOS_EDAD:
        raise ValueError(
            f"Grupo de edad desconocido: '{grupo_edad}'. Opciones: {', '.join(GRUPOS_EDAD)}"
        )
    return [
        p for p in pasajeros
        if (clase is None or p.clase == clase)
        and (grupo_edad is None or p.grupo_edad() == grupo_edad)
    ]


def resumir_grupo(grupo):
    cantidad = len(grupo)
    sobrevivientes = sum(1 for p in grupo if p.sobrevivio)
    proporcion = sobrevivientes / cantidad if cantidad > 0 else None
    return {
        "cantidad": cantidad,
        "sobrevivientes": sobrevivientes,
        "proporcion_sobrevivientes": proporcion,
    }


def verificar_resumen(resumen):
    if not 0 <= resumen["sobrevivientes"] <= resumen["cantidad"]:
        raise ValueError("El resumen tiene más sobrevivientes que pasajeros")
    proporcion = resumen["proporcion_sobrevivientes"]
    if resumen["cantidad"] == 0:
        if proporcion is not None:
            raise ValueError("Un grupo vacío no puede tener proporción")
    elif not 0 <= proporcion <= 1:
        raise ValueError(f"Proporción fuera de rango: {proporcion}")


def exportar_fichas(grupo, ruta):
    ruta = Path(ruta)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    columnas = ["PassengerId", "Nombre", "Billete", "Clase", "Edad", "GrupoEdad", "Sobrevivio"]
    with open(ruta, "w", encoding="utf-8", newline="") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=columnas)
        escritor.writeheader()
        for pasajero in grupo:
            escritor.writerow(pasajero.a_ficha())


def exportar_resumen(resumen, filtros, ruta):
    ruta = Path(ruta)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with open(ruta, "w", encoding="utf-8") as archivo:
        json.dump({"filtros": filtros, "resumen": resumen}, archivo, ensure_ascii=False, indent=2)


def guardar_rechazos(rechazos, ruta):
    ruta = Path(ruta)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with open(ruta, "w", encoding="utf-8", newline="") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=["fila", "PassengerId", "motivo"])
        escritor.writeheader()
        escritor.writerows(rechazos)
