import gzip
import csv
from pathlib import Path

def pregunta_05():
    """
    Para cada letra de la primera columna (`letter`), encuentre el valor
    máximo y el valor mínimo de la segunda columna (`value`). Retorne una lista
    de tuplas `(letra, máximo, mínimo)` ordenada alfabéticamente por la letra.

    Ejemplo del formato de la respuesta:

        [("A", 9, 2), ("B", 9, 1), ...]
    """
    ruta = Path(__file__).resolve().parent.parent / "data" / "data.csv.gz"
    conteo = {}

    with gzip.open(ruta, "rt") as archivo:
        lector = csv.reader(archivo, delimiter="\t")

        for fila in lector:
            letra = fila[0]
            valor = int(fila[1])
            if letra in conteo:
                max_val, min_val = conteo[letra]
                conteo[letra] = max(max_val, valor), min(min_val, valor)
            else:
                conteo[letra] = valor, valor

    resultado = sorted([(letra, max_val, min_val) for letra, (max_val, min_val) in conteo.items()])

    return resultado
