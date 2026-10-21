# tp2-ChicoskyPamela

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
- Lectura de CSV y JSON equivalentes con el conjunto "train" (se cambió el nombre a titanic.csv) de Kaggle (891 pasajeros).
- Búsqueda por identificador, filtros por clase y grupo de edad, resumen y exportación.
- Validación de billete, edad y supervivencia, con un registro de filas rechazadas.
- Una categoría "edad desconocida" para los 177 pasajeros sin edad registrada.

**Queda fuera:**
- Modelos predictivos o aprendizaje automático.
- Interfaz gráfica o web (solo consola).
- Completar o estimar edades faltantes.
- Los pasajeros del archivo test.csv de Kaggle (no tienen el dato de supervivencia) y la tripulación.
- Filtros por otras variables (sexo, puerto de embarque, tarifa), que podrían agregarse en una versión futura.