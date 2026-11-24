import gzip
import csv
from pathlib import Path

def pregunta_01():
    """
    Calcule la suma de los valores de la segunda columna (`value`) del
    archivo `data/data.csv.gz` y retorne el resultado como un número entero.

    Ejemplo del formato de la respuesta:

        214
    """
    ruta = Path(__file__).resolve().parent.parent / "data" / "data.csv.gz"
    suma = 0

    with gzip.open(ruta, "rt") as archivo:
        lector = csv.reader(archivo, delimiter="\t")

        for fila in lector:
            suma += int(fila[1])

    return suma
