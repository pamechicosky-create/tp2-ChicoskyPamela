import csv
import json
from abc import ABC, abstractmethod
from pathlib import Path

class FuenteDatos(ABC):
    extension = ""
    
    def cargar(self, ruta):
        ruta = Path(ruta)
        if not ruta.exists():
            raise FileNotFoundError(f"No se encontró el archivo de datos: {ruta}")
        if ruta.suffix.lower() != self.extension:
            raise ValueError(
                f"{type(self).__name__} espera un archivo {self.extension}, "
                f"pero recibió: {ruta.name}"
            )
        registros = self._leer(ruta)
        if not registros:
            raise ValueError(f"El archivo {ruta.name} no contiene registros.")
        return registros

    @abstractmethod
    def _leer(self, ruta):
        """Lee el archivo y devuelve una lista de diccionarios."""
        
class FuenteCSV(FuenteDatos):
    extension = ".csv"

    def _leer(self, ruta):
        with open(ruta, encoding="utf-8", newline="") as archivo:
            lector = csv.DictReader(archivo)
            return [dict(fila) for fila in lector]


class FuenteJSON(FuenteDatos):
    extension = ".json"

    def _leer(self, ruta):
        with open(ruta, encoding="utf-8") as archivo:
            try:
                contenido = json.load(archivo)
            except json.JSONDecodeError as error:
                raise ValueError(f"El archivo {ruta.name} no es un JSON válido: {error}")

        if not isinstance(contenido, list):
            raise ValueError(
                f"El archivo {ruta.name} debe contener una lista de objetos."
            )

        registros = []
        for posicion, objeto in enumerate(contenido):
            if not isinstance(objeto, dict):
                raise ValueError(
                    f"El elemento {posicion} de {ruta.name} no es un objeto."
                )
            registros.append(
                {clave: "" if valor is None else str(valor) for clave, valor in objeto.items()}
            )
        return registros


def obtener_fuente(ruta):
    fuentes = {".csv": FuenteCSV, ".json": FuenteJSON}
    extension = Path(ruta).suffix.lower()
    if extension not in fuentes:
        raise ValueError(
            f"Formato no soportado: '{extension}'. Use un archivo .csv o .json."
        )
    return fuentes[extension]()