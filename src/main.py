import argparse
import sys
from pathlib import Path

from fuentes import obtener_fuente
from pasajero import GRUPOS_EDAD
from pipeline import (
    buscar_pasajero,
    exportar_fichas,
    exportar_resumen,
    filtrar_grupo,
    guardar_rechazos,
    indexar_pasajeros,
    limpiar_datos,
    normalizar_campos,
    resumir_grupo,
    validar_esquema,
    verificar_resumen,
)

CARPETA_PROYECTO = Path(__file__).resolve().parent.parent
RUTA_DATOS = CARPETA_PROYECTO / "data" / "titanic.csv"
CARPETA_SALIDAS = CARPETA_PROYECTO / "outputs"


def cargar_pasajeros(ruta_datos):
    fuente = obtener_fuente(ruta_datos)
    registros = normalizar_campos(fuente.cargar(ruta_datos))
    validar_esquema(registros)
    pasajeros, rechazos = limpiar_datos(registros)
    guardar_rechazos(rechazos, CARPETA_SALIDAS / "rechazos.csv")
    print(f"Leídos {len(registros)} registros de {Path(ruta_datos).name}: "
          f"{len(pasajeros)} válidos, {len(rechazos)} rechazados.")
    return pasajeros


def mostrar_ficha(ficha):
    for campo, valor in ficha.items():
        print(f"  {campo:<12} {valor}")


def operacion_buscar(pasajeros, id_pasajero):
    indice = indexar_pasajeros(pasajeros)
    pasajero = buscar_pasajero(indice, id_pasajero)
    if pasajero is None:
        print(f"No existe ningún pasajero con PassengerId {id_pasajero}.")
        return
    print(f"Ficha del pasajero {id_pasajero}:")
    mostrar_ficha(pasajero.a_ficha())


def operacion_grupo(pasajeros, clase, grupo_edad):
    grupo = filtrar_grupo(pasajeros, clase, grupo_edad)
    resumen = resumir_grupo(grupo)
    verificar_resumen(resumen)

    filtros = {"clase": clase, "grupo_edad": grupo_edad}
    print(f"Filtros: clase={clase or 'todas'}, grupo de edad={grupo_edad or 'todos'}")
    if resumen["cantidad"] == 0:
        print("El grupo seleccionado no tiene pasajeros: no se puede calcular la proporción.")
        return

    print(f"  Pasajeros:      {resumen['cantidad']}")
    print(f"  Sobrevivientes: {resumen['sobrevivientes']}")
    print(f"  Proporción:     {resumen['proporcion_sobrevivientes']:.2f}")

    exportar_fichas(grupo, CARPETA_SALIDAS / "fichas_grupo.csv")
    exportar_resumen(resumen, filtros, CARPETA_SALIDAS / "resumen_grupo.json")
    print(f"Fichas y resumen guardados en {CARPETA_SALIDAS}")


def crear_parser():
    parser = argparse.ArgumentParser(
        description="Explorador de pasajeros del Titanic para actividades educativas."
    )
    parser.add_argument(
        "--datos", default=str(RUTA_DATOS),
        help="Archivo de datos .csv o .json (por defecto data/titanic.csv)",
    )
    operaciones = parser.add_subparsers(dest="operacion", required=True)

    buscar = operaciones.add_parser("buscar", help="Buscar un pasajero por PassengerId")
    buscar.add_argument("id", type=int, help="PassengerId del pasajero")

    grupo = operaciones.add_parser("grupo", help="Filtrar, resumir y exportar un grupo")
    grupo.add_argument("--clase", type=int, choices=[1, 2, 3], help="Clase del billete")
    grupo.add_argument("--edad", choices=GRUPOS_EDAD, help="Grupo de edad")
    return parser


def main():
    argumentos = crear_parser().parse_args()
    try:
        pasajeros = cargar_pasajeros(argumentos.datos)
        if argumentos.operacion == "buscar":
            operacion_buscar(pasajeros, argumentos.id)
        else:
            operacion_grupo(pasajeros, argumentos.clase, argumentos.edad)
    except (FileNotFoundError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
