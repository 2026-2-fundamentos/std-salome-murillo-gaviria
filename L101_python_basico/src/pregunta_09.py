import gzip
import csv
from pathlib import Path

def pregunta_09():
    """
    Cuente cuántas veces aparece cada clave en la quinta columna (`metrics`)
    de todo el archivo. Retorne un diccionario `{clave: cantidad}` con las
    claves en orden alfabético.

    Ejemplo del formato de la respuesta:

        {"aaa": 13, "bbb": 16, "ccc": 23, ...}
    """

    ruta = Path(__file__).resolve().parent.parent / "data" / "data.csv.gz"
    conteo = {}

    with gzip.open(ruta, "rt") as archivo:
        lector = csv.reader(archivo, delimiter="\t")

        for fila in lector:
            pares = fila[4].split(",") 
            for par in pares:
                clave, _ = par.split(":")
                conteo[clave] = conteo.get(clave, 0) + 1

    resultado = dict(sorted(conteo.items()))

    return resultado
