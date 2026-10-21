# Datos y su procedencia

## Fuente y procedencia

**URL:** https://www.kaggle.com/competitions/titanic/data?select=train.csv

**Responsable del dataset:** Kaggle.

**Licencia:** Sujeto a las reglas de la competencia.

**Origen:** Universidad de Vanderbilt (F. Harrell y T. Cason), basado en Encyclopedia Titanica.

**Fecha de consulta:** 21/10/2026

## Unidad de análisis y variables
Originalmente el dataset cuenta con 3 archivos CSV, solo nos será útil el llamado "train.csv" que luego se nombró como "titanic.csv".
Cada fila representa un pasajero del Titanic, cuenta con 891 filas y 12 columnas de las cuales solo se usarán:
- PassengerId | Identificador único del pasajero, entero de 1 a 891.
- Survived | Valores:  0 = NO, 1 = SI
- Pclass | Clase de billete, valores: 1, 2 o 3
- Name | Nombre completo del pasajero, incluye el título (Mr., Mrs., Miss.).
- Age | Edad en años, numérico decimal (de 0.42 a 80).
- Ticket | Número de billete, texto con formatos variados.

## Limitaciones y sesgos relevantes
- Edades faltantes: Hay 177 pasajeros sin edad que iran a la categoría "edad desconocida".
- Edades decimales: Los menores de un año presentan edades como, por ejemplo, 0.42. Kaggle menciona en las notas de las variables que las edades terminadas en .5 son estimadas.
- Debido a que el archivo no cuenta con toda la gente a bordo, sino que solo tiene presente a los pasajeros y que además, 177 sin edad no forman parte del resumen, no es posible abarcar a todas las personas del Titanic.
- Formato de billetes variados: Hay numéricos, con prefijos y otros con el valor LINE sin número.
- Hay 681 billetes distintos para 891 pasajeros porque las familias compartían billete, por eso se usa PassengerId como identificador y no el billete.
- Los datos provienen de datos reconstruidos por lo que pueden tener errores.