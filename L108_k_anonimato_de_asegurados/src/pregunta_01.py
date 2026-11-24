import pandas as pd
from pathlib import Path
import json

def evaluar_esquema(df, columnas):
    # Agrupar y contar las clases de equivalencia
    grupos = df.groupby(columnas, observed=True).size()

    equivalence_classes = len(grupos)
    k_before_suppression = grupos.min()

    # Identificar las clases que se deben suprimir
    clases_suprimidas = grupos[grupos < 5]
    suppressed_records = clases_suprimidas.sum()

    # Obtener los registros publicados
    clases_publicadas = grupos[grupos >= 5]

    df_publicado = df.merge(clases_publicadas.reset_index()[columnas],on=columnas,how='inner')

    published_records = len(df_publicado)
    published_classes = len(clases_publicadas)

    # Comprobar diversidad de fumadores
    diversidad = df_publicado.groupby(columnas, observed=True)['smoker'].nunique()
    clases_sin_diversidad = diversidad[diversidad == 1]
    classes_without_smoker_diversity = len(clases_sin_diversidad)
    records_without_smoker_diversity = grupos[grupos.index.isin(clases_sin_diversidad.index)].sum()

    resultado = {
        "quasi_identifiers": columnas,
        "equivalence_classes": int(equivalence_classes),
        "k_before_suppression": int(k_before_suppression),
        "suppressed_records": int(suppressed_records),
        "published_records": int(published_records),
        "published_classes": int(published_classes),
        "classes_without_smoker_diversity": int(classes_without_smoker_diversity),
        "records_without_smoker_diversity": int(records_without_smoker_diversity)
    }

    return resultado, df_publicado

def pregunta_01():
    """
    Una aseguradora quiere publicar datos de sus afiliados para que un grupo
    de investigación estudie el costo de los seguros, sin que nadie pueda
    reconocer a una persona. El archivo `data/insurance.csv.gz` tiene una fila
    por afiliado con su edad (`age`), sexo (`sex`), índice de masa corporal
    (`bmi`), número de hijos (`children`), si fuma (`smoker`), región
    (`region`) y el costo de su seguro (`charges`).

    El archivo no tiene nombres ni documentos, pero eso no basta: la edad, el
    sexo, el índice de masa corporal, el número de hijos y la región son
    cuasi-identificadores, porque combinados pueden señalar a una persona.
    `smoker` es el atributo sensible que se quiere proteger.

    En este laboratorio usted va a medir el riesgo de reidentificación y a
    decidir qué publicar. Use estas definiciones:

    - Una clase de equivalencia es un grupo de registros con los mismos
      valores en todos los cuasi-identificadores. Un conjunto de datos cumple
      k-anonimato si toda clase tiene al menos k registros. Use k = 5.
    - `age_group`: `18-29`, `30-39`, `40-49` o `50-64`.
    - `bmi_group`: `bajo peso` (menos de 18.5), `normal` (desde 18.5 y menos
      de 25), `sobrepeso` (desde 25 y menos de 30) u `obesidad` (30 o más).
    - `children_group`: `0`, `1-2` o `3+`.

    Evalúe dos esquemas de generalización:

    - `with_children`: `age_group`, `sex`, `bmi_group`, `children_group` y
      `region`.
    - `without_children`: `age_group`, `sex`, `bmi_group` y `region`; el
      número de hijos no se publica.

    En cada esquema, suprima (no publique) los registros de las clases con
    menos de 5 registros. Luego, entre las clases publicadas, identifique las
    que no tienen diversidad en el atributo sensible, es decir, aquellas en
    las que todos los afiliados fuman o ninguno fuma: en esas clases, saber
    que alguien pertenece a ellas revela si fuma.

    Escriba `submission/privacy_report.json` con estas claves:

    - `original_k`: el menor tamaño de clase usando los cuasi-identificadores
      originales, sin generalizar.
    - `original_unique_records`: cuántos registros son los únicos de su clase
      con los cuasi-identificadores originales.
    - `schemes`: un diccionario con una entrada por esquema (`with_children` y
      `without_children`), cada una con las claves `quasi_identifiers` (la
      lista de columnas del esquema), `equivalence_classes` (clases antes de
      suprimir), `k_before_suppression`, `suppressed_records`,
      `published_records`, `published_classes`,
      `classes_without_smoker_diversity` y
      `records_without_smoker_diversity`.
    - `selected_scheme`: el esquema que suprime menos registros.
    - `mean_charges_original` y `mean_charges_published`: el costo promedio
      de todos los afiliados y el de los registros publicados con el esquema
      seleccionado.
    - `smoker_rate_original` y `smoker_rate_published`: la proporción de
      fumadores en ambos casos.

    Escriba también `submission/insurance_published.csv`, sin el índice de
    Pandas, con los registros publicados del esquema seleccionado, en el
    mismo orden del archivo original, y las columnas del esquema seguidas de
    `smoker` y `charges`.

    La función también debe retornar el reporte como un diccionario.

    Ejemplo del formato del reporte:

        {
          "original_k": 1,
          "original_unique_records": 1330,
          "schemes": {
            "with_children": {
              "quasi_identifiers": ["age_group", "sex", ...],
              "equivalence_classes": 278,
              ...
            },
            ...
          },
          ...
        }
    """
    ruta = Path(__file__).resolve().parent.parent / "data" / "insurance.csv.gz"
    df = pd.read_csv(ruta)

    con_hijos = df.groupby(['age', 'sex', 'bmi', 'children', 'region']).size()
    
    original_k = con_hijos.min()
    original_unique_records = con_hijos[con_hijos == 1].sum()

# anonimizacion de la edad
    df['age_group'] = pd.cut(
        df['age'],
        bins=[18, 30, 40, 50, 65],
        labels=['18-29', '30-39', '40-49', '50-64'],
        right=False
    )

# anonimizacion del indice de masa corporal
    df['bmi_group'] = pd.cut(
        df['bmi'],
        bins=[-float('inf'), 18.5, 25, 30, float('inf')],
        labels=['bajo peso', 'normal', 'sobrepeso', 'obesidad'],
        right=False
    )

# anonimizacion del numero de hijos
    df['children_group'] = pd.cut(
        df['children'],
        bins=[-1, 0, 2, float('inf')],
        labels=['0', '1-2', '3+'],
    )

    columnas_con_hijos = ['age_group', 'sex', 'bmi_group', 'children_group', 'region']
    columnas_sin_hijos = ['age_group', 'sex', 'bmi_group', 'region']

    resultado_con_hijos, df_con_hijos = evaluar_esquema(df, columnas_con_hijos)
    resultado_sin_hijos, df_sin_hijos = evaluar_esquema(df, columnas_sin_hijos)

    schemes = {
        "with_children": resultado_con_hijos,
        "without_children": resultado_sin_hijos
    }

    if resultado_con_hijos["suppressed_records"] <= resultado_sin_hijos["suppressed_records"]:
        selected_scheme = "with_children"
        df_publicado = df_con_hijos
        columnas_seleccionadas = columnas_con_hijos
    else:
        selected_scheme = "without_children"
        df_publicado = df_sin_hijos
        columnas_seleccionadas = columnas_sin_hijos

    mean_charges_original = df["charges"].mean()
    mean_charges_published = df_publicado["charges"].mean()

    smoker_rate_original = (df["smoker"] == "yes").mean()
    smoker_rate_published = (df_publicado["smoker"] == "yes").mean()

    reporte = {
        "original_k": int(original_k),
        "original_unique_records": int(original_unique_records),
        "schemes": schemes,
        "selected_scheme": selected_scheme,
        "mean_charges_original": float(mean_charges_original),
        "mean_charges_published": float(mean_charges_published),
        "smoker_rate_original": float(smoker_rate_original),
        "smoker_rate_published": float(smoker_rate_published)
    }

    ruta_salida = Path(__file__).resolve().parent.parent / "submission"

    with open(ruta_salida / "privacy_report.json", "w", encoding="utf-8") as archivo:
        json.dump(reporte, archivo, indent=4, ensure_ascii=False)

    columnas_csv = columnas_seleccionadas + ["smoker", "charges"]

    df_publicado[columnas_csv].to_csv(ruta_salida / "insurance_published.csv",index=False)

    return reporte
