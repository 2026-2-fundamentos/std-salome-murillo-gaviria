import gzip
import csv
from pathlib import Path

def pregunta_07():
    """
    Para cada valor distinto de la segunda columna (`value`), construya la
    lista de letras de la primera columna (`letter`) que aparecen con ese
    valor. Conserve las letras repetidas y el orden en que aparecen en el
    archivo. Retorne una lista de tuplas `(valor, letras)` ordenada por el
    valor.

    Ejemplo del formato de la respuesta:

        [(0, ["C"]), (1, ["E", "B", "E"]), (2, ["A", "E"]), ...]
    """

    ruta = Path(__file__).resolve().parent.parent / "data" / "data.csv.gz"
    listas = {}

    with gzip.open(ruta, "rt") as archivo:
        lector = csv.reader(archivo, delimiter="\t")

        for fila in lector:
            numero = int(fila[1])
            letra = fila[0]
            if numero in listas:
                listas[numero].append(letra)
            else:
                listas[numero] = [letra]

    resultado = sorted(listas.items())

    return resultado
