import gzip
import csv
from pathlib import Path

def pregunta_06():
    """
    La quinta columna (`metrics`) contiene pares `clave:valor` separados por
    comas. Para cada clave, encuentre el valor mínimo y el valor máximo que
    aparecen en todo el archivo. Retorne una lista de tuplas
    `(clave, mínimo, máximo)` ordenada alfabéticamente por la clave.

    Observe que el orden es mínimo y luego máximo, al contrario de la
    pregunta 5.

    Ejemplo del formato de la respuesta:

        [("aaa", 1, 9), ("bbb", 1, 9), ...]
    """
    ruta = Path(__file__).resolve().parent.parent / "data" / "data.csv.gz"
    conteo = {}

    with gzip.open(ruta, "rt") as archivo:
        lector = csv.reader(archivo, delimiter="\t")

        for fila in lector:
            pares = fila[4].split(",") 
            for par in pares:
                clave, valor = par.split(":")
                valor = int(valor)
                if clave in conteo:
                    min_val, max_val = conteo[clave]
                    conteo[clave] = (min(min_val, valor), max(max_val, valor))
                else:
                    conteo[clave] = (valor, valor)

    resultado = sorted([(clave, min_val, max_val) for clave, (min_val, max_val) in conteo.items()])

    return resultado
