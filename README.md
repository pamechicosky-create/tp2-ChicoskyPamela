# tp2-ChicoskyPamela

## **Explorador de pasajeros del Titanic**

Pamela Chicosky | Programación Orientada a Datos | UCA

## 1. PROBLEMA Y ALCANCE

**Problema:** Una persona que prepara una actividad sobre el Titanic necesita encontrar pasajeros concretos, armar grupos según clase y edad y saber qué proporción de cada grupo sobrevivió. Eso implica buscar y contar a mano en un archivo de 891 filas, lo que hace que sea un trabajo donde es fácil equivocarse y cuesta repetir la actividad cuando cambian los criterios del grupo.

**Usuarios:** Docentes o estudiantes que necesiten usar el caso Titanic para fines educativos.

**Solución propuesta:** Un explorador de pasajeros que permite:

- Buscar un pasajero por su identificador (PassengerId) y mostrar su ficha: nombre, billete, clase, edad, grupo de edad y si sobrevivió. Si el identificador no existe, lo informa con un mensaje claro.
- Filtrar un grupo por clase (1, 2 o 3) y/o grupo de edad (niño (0-12), adolescente (13-17), adulto (18-59), mayor (60 o más) o edad desconocida).
- Resumir el grupo filtrado: cantidad de pasajeros, cantidad de sobrevivientes y proporción de sobrevivientes.
- Exportar las fichas y el resumen del grupo seleccionado a un archivo (CSV/JSON) para usarlo en clase.

**Resultado y interpretación:**

- Ficha de pasajero: datos de una persona.
- Resumen de grupo: por ejemplo "3ra clase, niños: N pasajeros, S sobrevivientes, proporción S/N". La proporción va de 0 a 1 e indica qué parte del grupo sobrevivió. Sirve para comparar grupos entre sí.
- Si un grupo no tiene pasajeros, el programa lo dice en vez de devolver 0 o fallar.
- La proporción describe lo que pasó en este conjunto de datos y no permite predecir nada ni establecer causas.

**Alcance de la primera versión:**

**Incluye:**

- Lectura de CSV y JSON equivalentes con el conjunto "train" (luego se cambió el nombre a titanic.csv) de Kaggle (891 pasajeros).
- Búsqueda por identificador, filtros por clase y grupo de edad, resumen y exportación.
- Validación de billete, edad y supervivencia, con un registro de filas rechazadas.
- Una categoría "edad desconocida" para los 177 pasajeros sin edad registrada.

**Queda fuera:**

- Modelos predictivos o aprendizaje automático.
- Interfaz gráfica o web (solo consola).
- Completar o estimar edades faltantes.
- Los pasajeros del archivo test.csv de Kaggle (no tienen el dato de supervivencia) y la tripulación.
- Filtros por otras variables (sexo, puerto de embarque, tarifa), que podrían agregarse en una versión futura.

## 2. DATOS

Pasajeros del Titanic (conjunto "train" de la competencia Titanic de Kaggle, 891 pasajeros, una fila por pasajero). Fuente, licencia, variables y limitaciones en [data/README.md](data/README.md).

- `data/titanic.csv`: archivo original descargado de Kaggle.
- `data/titanic.json`: copia equivalente (lista de objetos con las mismas columnas), generada con `python src/generar_json.py`.

## 3. INSTALACIÓN

Requisitos: Python 3.10 o superior. El programa usa solo la biblioteca estándar (csv, json, re, argparse, pathlib, unittest), así que no hace falta instalar paquetes.

```
git clone https://github.com/pamechicosky-create/tp2-ChicoskyPamela.git
cd tp2-ChicoskyPamela
```

## 4. Uso

Todos los comandos se ejecutan desde la carpeta principal del proyecto.

**Buscar un pasajero por su identificador:**

```
python src/main.py buscar 5
```

**Filtrar, resumir y exportar un grupo** (los dos filtros son opcionales):

```
python src/main.py grupo --clase 3 --edad nino
python src/main.py grupo --clase 1
python src/main.py grupo --edad desconocida
```

Grupos de edad: `nino`, `adolescente`, `adulto`, `mayor`, `desconocida`.

**Usar el archivo JSON en lugar del CSV:**

```
python src/main.py --datos data/titanic.json grupo --clase 2
```

**Regenerar el JSON a partir del CSV:**

```
python src/generar_json.py
```

**Ejecutar las pruebas:**

```
python -m unittest discover -s tests -v
```

### Archivos de salida

Se guardan en `outputs/` (carpeta excluida del repositorio con `.gitignore`, porque se regenera en cada ejecución):

| Archivo | Contenido |
|---|---|
| `fichas_grupo.csv` | Una ficha por pasajero del grupo filtrado |
| `resumen_grupo.json` | Filtros aplicados, cantidad, sobrevivientes y proporción |
| `rechazos.csv` | Filas descartadas en la limpieza, con número de fila, PassengerId y motivo |

## 5. Ejemplo de resultado

```
> python src/main.py grupo --clase 3 --edad nino
Leídos 891 registros de titanic.csv: 891 válidos, 0 rechazados.
Filtros: clase=3, grupo de edad=nino
  Pasajeros:      48
  Sobrevivientes: 20
  Proporción:     0.42
```

Proporción de sobrevivientes por clase y grupo de edad, calculada con el programa:

| Grupo de edad | 1.ª clase | 2.ª clase | 3.ª clase |
|---|---|---|---|
| Niño (0-12) | 3/4 (0.75) | 17/17 (1.00) | 20/48 (0.42) |
| Adolescente (13-17) | 8/8 (1.00) | 4/6 (0.67) | 9/30 (0.30) |
| Adulto (18-59) | 106/157 (0.68) | 61/146 (0.42) | 55/272 (0.20) |
| Mayor (60+) | 5/17 (0.29) | 1/4 (0.25) | 1/5 (0.20) |
| Edad desconocida | 14/30 (0.47) | 4/11 (0.36) | 34/136 (0.25) |
| **Total de la clase** | **136/216 (0.63)** | **87/184 (0.47)** | **119/491 (0.24)** |

**Interpretación:** en todos los grupos de edad, la 3.ª clase tiene la proporción de sobrevivientes más baja, y en el total por clase la proporción baja de 1.ª (0.63) a 2.ª (0.47) y a 3.ª (0.24). Por ejemplo, sobrevivieron todos los niños de 2.ª clase, pero menos de la mitad de los de 3.ª. Algunos grupos son muy chicos (4 niños de 1.ª clase, 4 mayores de 2.ª), así que sus proporciones cambian mucho con un solo pasajero y hay que leerlas con cuidado.

## 6. Organización del código

```
tp2-ChicoskyPamela/
├── README.md
├── requirements.txt
├── .gitignore
├── data/
│   ├── README.md          documentación de la fuente y las variables
│   ├── titanic.csv
│   └── titanic.json
├── src/
│   ├── fuentes.py         FuenteDatos (abstracta), FuenteCSV, FuenteJSON, obtener_fuente()
│   ├── pasajero.py        clase Pasajero (grupo de edad y ficha)
│   ├── pipeline.py        validación, limpieza, búsqueda, filtros, resumen y exportación
│   ├── main.py            punto de entrada por línea de comandos
│   └── generar_json.py    genera titanic.json a partir de titanic.csv
└── tests/
    └── test_titanic.py    pruebas con unittest
```

**Flujo de procesamiento** (leer → validar → limpiar → analizar → comunicar):

1. `obtener_fuente(ruta)` elige `FuenteCSV` o `FuenteJSON` según la extensión, y `cargar()` devuelve una lista de diccionarios con el mismo formato para los dos.
2. `normalizar_campos()` quita espacios sobrantes y `validar_esquema()` comprueba que estén las columnas necesarias.
3. `limpiar_datos()` convierte cada fila en un `Pasajero` y separa las filas inválidas en una lista de rechazos con su motivo.
4. `indexar_pasajeros()` + `buscar_pasajero()`, o `filtrar_grupo()` + `resumir_grupo()` + `verificar_resumen()`.
5. `main.py` muestra el resultado y lo exporta a `outputs/`.

**Conceptos aplicados:**

- **Abstracción de fuentes:** `FuenteDatos` define el contrato `cargar(ruta)` y las subclases `FuenteCSV` y `FuenteJSON` implementan la lectura. El resto del programa no depende del formato del archivo.
- **Clase del dominio:** `Pasajero` reúne los datos de una persona y decide su grupo de edad (`grupo_edad()`) y su ficha (`a_ficha()`).
- **Expresión regular:** `PATRON_BILLETE` en `pipeline.py` (ver la sección de limpieza).
- **Funciones con una sola responsabilidad:** lectura, validación, limpieza, búsqueda, filtro, resumen y exportación están separadas.

## 7. Decisiones de limpieza

Cada fila se valida y, si no cumple una regla, se rechaza y se registra en `outputs/rechazos.csv` con su motivo:

| Campo | Regla | Si no se cumple |
|---|---|---|
| `PassengerId` | Entero positivo y sin repetir | Se rechaza la fila (el duplicado se rechaza; se conserva la primera aparición) |
| `Survived` | 0 o 1 | Se rechaza |
| `Pclass` | 1, 2 o 3 | Se rechaza |
| `Name` | No vacío | Se rechaza |
| `Age` | Número entre 0 (excluido) y 100 | Fuera de rango o no numérica: se rechaza. **Vacía: se acepta** y el pasajero va al grupo "desconocida" (no se inventa una edad) |
| `Ticket` | Coincide con la expresión regular | Se rechaza |

**Expresión regular del billete:** `^(?:[A-Za-z0-9./]+ ){0,2}\d{1,7}$|^LINE$`
Acepta hasta dos prefijos opcionales formados por letras, números, puntos o barras y separados por un espacio (como `PC`, `A/5`, `STON/O 2.`), seguidos de un número de 1 a 7 cifras. Ejemplos válidos: `330911`, `PC 17599`, `A/5 21171`, `STON/O 2. 3101294`. También acepta el valor especial `LINE`, que aparece en 4 billetes sin número. Rechaza, por ejemplo, un billete vacío, uno sin número (`ABC`) o uno con el prefijo pegado al número (`PC17599`). La regex solo comprueba el formato: no verifica que el billete haya existido.

**Resultado con los datos actuales:** las 891 filas pasan la validación (0 rechazos). Las reglas de rechazo se comprueban en las pruebas con filas inválidas preparadas a propósito.

## 8. Pruebas

`python -m unittest discover -s tests -v` ejecuta 19 pruebas:

- **Casos normales:** carga de los 891 pasajeros, búsqueda de un ID existente, filtro por clase.
- **Entradas inválidas y casos límite:** ID ausente, edad faltante, billetes inválidos, supervivencia o clase fuera de rango, edad negativa, ID duplicado, columna faltante, archivo inexistente, formato no soportado, JSON mal formado, filtro con parámetro inválido.
- **Propiedades del resultado:** 2 sobrevivientes de 4 da 0.5; un grupo vacío da una respuesta explícita; CSV y JSON producen los mismos pasajeros; los grupos de edad suman el total; las proporciones están entre 0 y 1.

## 9. Limitaciones

- 177 pasajeros no tienen edad, así que los resúmenes por edad no los incluyen salvo en el grupo "desconocida".
- El archivo tiene 891 de los 1309 pasajeros registrados y no incluye a la tripulación: los resultados describen este conjunto, no a todas las personas a bordo.
- Algunos grupos son muy pequeños y sus proporciones son poco estables.
- Los resultados son descriptivos: no explican causas ni sirven para predecir.
- La regex valida el formato del billete, pero no su existencia real.
