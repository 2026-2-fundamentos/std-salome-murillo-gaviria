import pandas as pd
from pathlib import Path

def pregunta_01():
    """
    Las frases de este laboratorio no están en una tabla, sino en miles de
    archivos de texto organizados en carpetas. Dentro de `data/` hay dos
    carpetas, `train/` y `test/`, y cada una contiene las carpetas
    `negative/`, `neutral/` y `positive/`. Cada archivo `.txt` contiene una
    frase, y la carpeta donde se encuentra indica su sentimiento.

    Su tarea es construir un dataset para cada división y guardarlo en:

    - `submission/train_dataset.csv`
    - `submission/test_dataset.csv`

    Cada archivo debe tener dos columnas: `phrase`, con el texto de la frase,
    y `target`, con el nombre de la carpeta de sentimiento (`negative`,
    `neutral` o `positive`). Recorra las carpetas y los archivos en orden
    alfabético, de modo que el resultado sea siempre el mismo. No guarde el
    índice de Pandas en el CSV.

    Ejemplo del formato de cada archivo:

        phrase,target
        "The real estate company posted a net loss ...",negative
        ...
        "Cardona slowed her vehicle , turned around ...",neutral
        ...
    """

    def recorrer_archivos(ruta, lista):
        for sentimiento in sorted(ruta.iterdir()):
            for archivo in sorted(sentimiento.glob("*.txt")):
                with open(archivo, "r", encoding="utf-8") as f:
                    frase = f.read().strip()
                    lista.append({"phrase": frase, "target": sentimiento.name})

    def crear_csv(lista, nombre_archivo):
        dataframe = pd.DataFrame(lista)
        dataframe.to_csv(Path(__file__).resolve().parent.parent / "submission" / nombre_archivo, index=False)

    ruta1 = Path(__file__).resolve().parent.parent / "data" / "train"
    ruta2 = Path(__file__).resolve().parent.parent / "data" / "test"

    train = []
    test = []

    recorrer_archivos(ruta1, train)
    recorrer_archivos(ruta2, test)

    crear_csv(train, "train_dataset.csv")
    crear_csv(test, "test_dataset.csv")
