import gzip
import csv
from pathlib import Path

def pregunta_10():
    """
    Para cada registro del archivo, en el mismo orden en que aparecen,
    retorne una tupla con la letra de la primera columna (`letter`), la
    cantidad de elementos de la cuarta columna (`codes`) y la cantidad de
    pares de la quinta columna (`metrics`). El resultado es una lista con una
    tupla por registro.

    Ejemplo del formato de la respuesta:

        [("E", 3, 5), ("A", 3, 4), ("B", 4, 4), ...]
    """

    ruta = Path(__file__).resolve().parent.parent / "data" / "data.csv.gz"
    conteo = []

    with gzip.open(ruta, "rt") as archivo:
        lector = csv.reader(archivo, delimiter="\t")

        for fila in lector:
            letra = fila[0]
            codigos = len(fila[3].split(","))
            metricas = len(fila[4].split(","))
            conteo.append((letra, codigos, metricas))

    return conteo
