import pandas as pd
from pathlib import Path

def pregunta_06():
    """
    Usando `data/tbl1.tsv`, obtenga los valores distintos de la columna `c4`,
    conviértalos a mayúsculas y retórnelos como una lista ordenada
    alfabéticamente.

    Ejemplo del formato de la respuesta:

        ["A", "B", "C", "D", "E", "F", "G"]
    """

    ruta = Path(__file__).resolve().parent.parent / "data" / "tbl1.tsv"
    df = pd.read_csv(ruta, sep="\t")
    
    valores = sorted(df["c4"].str.upper().unique())

    return valores
