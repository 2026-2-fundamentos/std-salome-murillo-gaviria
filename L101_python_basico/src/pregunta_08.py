import gzip
import csv
from pathlib import Path

def pregunta_08():
    """
    Repita la pregunta 7, pero ahora cada lista de letras debe contener cada
    letra una sola vez y estar ordenada alfabéticamente. Retorne una lista de
    tuplas `(valor, letras)` ordenada por el valor.

    Ejemplo del formato de la respuesta:

        [(0, ["C"]), (1, ["B", "E"]), (2, ["A", "E"]), ...]
    """

    ruta = Path(__file__).resolve().parent.parent / "data" / "data.csv.gz"
    listas = {}

    with gzip.open(ruta, "rt") as archivo:
        lector = csv.reader(archivo, delimiter="\t")

        for fila in lector:
            numero = int(fila[1])
            letra = fila[0]
            if (numero in listas) and (letra not in listas[numero]):
                listas[numero].append(letra)
            elif numero not in listas:
                listas[numero] = [letra]

    resultado = sorted([(numero, sorted(letras)) for numero, letras in listas.items()])

    return resultado
