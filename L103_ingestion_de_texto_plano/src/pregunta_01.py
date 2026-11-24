import pandas as pd
import re
from pathlib import Path

def pregunta_01():
    """
    El archivo `data/clusters_report.txt` es un reporte de clústeres de
    palabras clave pensado para ser leído por una persona, no por un programa:
    los encabezados ocupan varias líneas, las columnas están alineadas con
    espacios y la lista de palabras clave de un clúster continúa en las líneas
    siguientes.

    Su tarea es convertir ese reporte en un DataFrame de Pandas con una fila
    por clúster y las columnas:

    - `cluster`: número del clúster, como entero.
    - `cantidad_de_palabras_clave`: como entero.
    - `porcentaje_de_palabras_clave`: como número decimal; por ejemplo, el
      texto `15,9 %` debe quedar como `15.9`.
    - `principales_palabras_clave`: todas las palabras clave del clúster en un
      solo texto, separadas por una coma y un único espacio.

    Retorne el DataFrame.

    Ejemplo del formato de la respuesta (se omite la última columna):

           cluster  cantidad_de_palabras_clave  porcentaje_de_palabras_clave
        0        1                         105                          15.9
        1        2                         102                          15.4
        ...
    """
    ruta = Path(__file__).resolve().parent.parent / "data" / "clusters_report.txt"

    with open(ruta, "rt") as archivo:
        lector = archivo.readlines()

    datos = []
    cluster = None

    for linea in lector:
        coincidencia = re.match(r"^\s*(\d+)\s+(\d+)\s+([\d,]+)\s*%\s+(.*)$",linea)

        if coincidencia:
            if cluster is not None:
                datos.append(cluster)

            cluster = {
                "cluster": int(coincidencia.group(1)),
                "cantidad_de_palabras_clave": int(coincidencia.group(2)),
                "porcentaje_de_palabras_clave": float(
                    coincidencia.group(3).replace(",", ".")
                ),
                "principales_palabras_clave": coincidencia.group(4).strip()
            }

        elif cluster is not None:
            cluster["principales_palabras_clave"] += " " + linea.strip()

    if cluster is not None:
        datos.append(cluster)

    for cluster in datos:
        palabras = cluster["principales_palabras_clave"]
        palabras = re.sub(r"\s+", " ", palabras).strip()
        palabras = palabras.rstrip(".")
        cluster["principales_palabras_clave"] = palabras

    dataframe = pd.DataFrame(datos)

    return dataframe
