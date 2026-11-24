import gzip
import csv
from pathlib import Path

def pregunta_12():
    """
    Para cada letra de la primera columna (`letter`), sume todos los valores
    numéricos de los pares `clave:valor` de la quinta columna (`metrics`).
    Retorne un diccionario `{letra: suma}` con las letras en orden alfabético.

    Ejemplo del formato de la respuesta:

        {"A": 177, "B": 187, "C": 114, ...}
    """

    ruta = Path(__file__).resolve().parent.parent / "data" / "data.csv.gz"
    conteo = {}

    with gzip.open(ruta, "rt") as archivo:
        lector = csv.reader(archivo, delimiter="\t")

        for fila in lector:
            letras = fila[0]
            metrics = fila[4].split(",")
            for metric in metrics:
                _, valor = metric.split(":")
                valor = int(valor)
                conteo[letras] = conteo.get(letras, 0) + valor

    resultado = dict(sorted(conteo.items()))

    return resultado
