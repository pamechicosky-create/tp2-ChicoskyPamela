import json
from pathlib import Path

from fuentes import FuenteCSV

CARPETA_DATOS = Path(__file__).resolve().parent.parent / "data"
RUTA_CSV = CARPETA_DATOS / "titanic.csv"
RUTA_JSON = CARPETA_DATOS / "titanic.json"


def generar_json(ruta_csv, ruta_json):
    registros = FuenteCSV().cargar(ruta_csv)
    registros_json = [
        {clave: (valor if valor != "" else None) for clave, valor in fila.items()}
        for fila in registros
    ]
    with open(ruta_json, "w", encoding="utf-8") as archivo:
        json.dump(registros_json, archivo, ensure_ascii=False, indent=2)
    return len(registros_json)


if __name__ == "__main__":
    cantidad = generar_json(RUTA_CSV, RUTA_JSON)
    print(f"Se guardaron {cantidad} registros en {RUTA_JSON}")
