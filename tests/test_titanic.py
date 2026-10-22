import json
import sys
import tempfile
import unittest
from pathlib import Path

CARPETA_PROYECTO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(CARPETA_PROYECTO / "src"))

from fuentes import FuenteCSV, FuenteJSON, obtener_fuente
from pasajero import Pasajero
from pipeline import (
    billete_valido,
    buscar_pasajero,
    filtrar_grupo,
    indexar_pasajeros,
    limpiar_datos,
    normalizar_campos,
    resumir_grupo,
    validar_esquema,
    verificar_resumen,
)

RUTA_CSV = CARPETA_PROYECTO / "data" / "titanic.csv"
RUTA_JSON = CARPETA_PROYECTO / "data" / "titanic.json"


def fila(id_pasajero="1", sobrevivio="1", clase="1", edad="30", billete="PC 17599"):
    return {
        "PassengerId": id_pasajero, "Survived": sobrevivio, "Pclass": clase,
        "Name": "Pasajero de prueba", "Age": edad, "Ticket": billete,
    }


def pasajero(id_pasajero, sobrevivio, clase=3, edad=30.0):
    return Pasajero(id_pasajero, "Prueba", "12345", clase, edad, sobrevivio)


def cargar(ruta):
    registros = normalizar_campos(obtener_fuente(ruta).cargar(ruta))
    validar_esquema(registros)
    return limpiar_datos(registros)


class TestCasosNormales(unittest.TestCase):
    def setUp(self):
        self.pasajeros, self.rechazos = cargar(RUTA_CSV)
        self.indice = indexar_pasajeros(self.pasajeros)

    def test_carga_todos_los_pasajeros(self):
        self.assertEqual(len(self.pasajeros), 891)
        self.assertEqual(self.rechazos, [])

    def test_buscar_id_existente(self):
        encontrado = buscar_pasajero(self.indice, 5)
        self.assertEqual(encontrado.nombre, "Allen, Mr. William Henry")
        self.assertEqual(encontrado.clase, 3)

    def test_buscar_id_ausente(self):
        self.assertIsNone(buscar_pasajero(self.indice, 9999))

    def test_filtro_por_clase(self):
        grupo = filtrar_grupo(self.pasajeros, clase=1)
        self.assertEqual(len(grupo), 216)
        self.assertTrue(all(p.clase == 1 for p in grupo))


class TestEdadYGrupos(unittest.TestCase):
    def test_grupos_de_edad(self):
        self.assertEqual(pasajero(1, True, edad=0.42).grupo_edad(), "nino")
        self.assertEqual(pasajero(1, True, edad=12).grupo_edad(), "nino")
        self.assertEqual(pasajero(1, True, edad=13).grupo_edad(), "adolescente")
        self.assertEqual(pasajero(1, True, edad=18).grupo_edad(), "adulto")
        self.assertEqual(pasajero(1, True, edad=60).grupo_edad(), "mayor")

    def test_edad_faltante_va_a_desconocida(self):
        pasajeros, rechazos = limpiar_datos([fila(edad="")])
        self.assertEqual(rechazos, [])
        self.assertIsNone(pasajeros[0].edad)
        self.assertEqual(pasajeros[0].grupo_edad(), "desconocida")

    def test_filtro_con_edad_faltante(self):
        grupo = [pasajero(1, True, edad=None), pasajero(2, False, edad=40)]
        self.assertEqual(len(filtrar_grupo(grupo, grupo_edad="desconocida")), 1)
        self.assertEqual(len(filtrar_grupo(grupo, grupo_edad="adulto")), 1)


class TestEntradasInvalidas(unittest.TestCase):
    def test_regex_billete(self):
        for billete in ("A/5 21171", "PC 17599", "330911", "STON/O2. 3101282", "LINE"):
            self.assertTrue(billete_valido(billete), billete)
        for billete in ("", "ABC", "PC17599", "12 34 56 78"):
            self.assertFalse(billete_valido(billete), billete)

    def test_filas_invalidas_se_rechazan_con_motivo(self):
        registros = [
            fila(id_pasajero="1"),
            fila(id_pasajero="2", sobrevivio="2"),
            fila(id_pasajero="3", clase="4"),
            fila(id_pasajero="4", edad="-5"),
            fila(id_pasajero="5", billete="sin numero"),
            fila(id_pasajero="1"),
        ]
        pasajeros, rechazos = limpiar_datos(registros)
        self.assertEqual(len(pasajeros), 1)
        self.assertEqual(len(rechazos), 5)
        self.assertIn("duplicado", rechazos[-1]["motivo"])

    def test_columna_faltante(self):
        registros = [fila()]
        del registros[0]["Ticket"]
        with self.assertRaises(ValueError):
            validar_esquema(registros)

    def test_archivo_inexistente(self):
        with self.assertRaises(FileNotFoundError):
            FuenteCSV().cargar("no_existe.csv")

    def test_formato_no_soportado(self):
        with self.assertRaises(ValueError):
            obtener_fuente("datos.txt")

    def test_json_que_no_es_lista(self):
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = Path(carpeta) / "malo.json"
            ruta.write_text(json.dumps({"PassengerId": 1}), encoding="utf-8")
            with self.assertRaises(ValueError):
                FuenteJSON().cargar(ruta)

    def test_filtro_con_parametro_invalido(self):
        with self.assertRaises(ValueError):
            filtrar_grupo([], clase=5)


class TestPropiedadesDelResultado(unittest.TestCase):
    def test_dos_de_cuatro_da_0_5(self):
        grupo = [pasajero(1, True), pasajero(2, True), pasajero(3, False), pasajero(4, False)]
        resumen = resumir_grupo(grupo)
        self.assertEqual(resumen["cantidad"], 4)
        self.assertEqual(resumen["sobrevivientes"], 2)
        self.assertEqual(resumen["proporcion_sobrevivientes"], 0.5)

    def test_grupo_vacio_tiene_respuesta_explicita(self):
        resumen = resumir_grupo([])
        self.assertEqual(resumen["cantidad"], 0)
        self.assertIsNone(resumen["proporcion_sobrevivientes"])
        verificar_resumen(resumen)

    def test_csv_y_json_son_equivalentes(self):
        pasajeros_csv, _ = cargar(RUTA_CSV)
        pasajeros_json, _ = cargar(RUTA_JSON)
        fichas_csv = [p.a_ficha() for p in pasajeros_csv]
        fichas_json = [p.a_ficha() for p in pasajeros_json]
        self.assertEqual(fichas_csv, fichas_json)

    def test_grupos_de_edad_conservan_el_total(self):
        pasajeros, _ = cargar(RUTA_CSV)
        total = sum(
            len(filtrar_grupo(pasajeros, grupo_edad=g))
            for g in ("nino", "adolescente", "adulto", "mayor", "desconocida")
        )
        self.assertEqual(total, len(pasajeros))

    def test_proporciones_en_rango(self):
        pasajeros, _ = cargar(RUTA_CSV)
        for clase in (1, 2, 3):
            resumen = resumir_grupo(filtrar_grupo(pasajeros, clase=clase))
            verificar_resumen(resumen)
            self.assertTrue(0 <= resumen["proporcion_sobrevivientes"] <= 1)


if __name__ == "__main__":
    unittest.main()
