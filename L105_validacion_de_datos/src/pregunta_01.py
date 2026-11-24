from pathlib import Path
import pandas as pd
import json
import re

def main():
  """
    Antes de limpiar o analizar un conjunto de datos, un analista debe
    documentar qué problemas tiene. En este laboratorio usted no va a limpiar
    `data/ventas.csv.gz`: va a construir un reporte de calidad que deje evidencia
    de sus problemas, tal como están en el archivo.

    Lea `data/ventas.csv.gz` sin modificar sus valores. Para trabajar con los
    encabezados, normalícelos: páselos a minúsculas, elimine los espacios al
    inicio y al final (y cualquier marca BOM) y reemplace los espacios
    internos por `_`. Las columnas requeridas son `supplier_id`, `supplier`,
    `country`, `city`, `purchase_date`, `amount`, `discount`, `weight`,
    `units`, `unit_price` y `contact_email`.

    Escriba el reporte en `submission/data_quality_report.json` con estas
    claves:

    - `row_count`: cantidad de filas de datos.
    - `column_count`: cantidad de columnas.
    - `missing_required_columns`: lista ordenada de columnas requeridas que no
      están en el archivo.
    - `unexpected_columns`: lista ordenada de columnas del archivo que no son
      requeridas.
    - `duplicate_row_count`: cantidad de filas idénticas a una fila anterior.
    - `duplicate_supplier_id_row_count`: cantidad de filas cuyo `supplier_id`
      aparece más de una vez (cuente todas esas filas, no solo las
      repetidas).
    - `missing_value_count_by_column`: diccionario con la cantidad de valores
      faltantes de cada columna. Considere faltantes las celdas vacías y las
      que contienen `N/A`.
    - `invalid_email_count`: cantidad de valores de `contact_email` que no
      tienen la forma `usuario@dominio.extension`.
    - `invalid_unit_count`: cantidad de valores numéricos de `units` que no son
      enteros positivos. Los valores faltantes no se cuentan aquí.
    - `country_values`: lista ordenada de los valores distintos de `country`,
      escritos exactamente como aparecen en el archivo.

    La función también debe retornar el reporte como un diccionario.

    Ejemplo del formato del reporte:

        {
          "row_count": 103,
          "column_count": 11,
          "missing_required_columns": [],
          ...
          "country_values": [" Colombia ", "CO", ...]
        }
  """

  ruta = Path(__file__).resolve().parent.parent / "data" / "ventas.csv.gz"
  df = pd.read_csv(ruta, dtype=str, keep_default_na=False)

  columnas = []

  for col in df.columns:
    col = col.strip().lower().replace(" ", "_")
    columnas.append(col)

  df.columns = columnas

  COLUMNAS_REQUERIDAS = [
    "supplier_id",
    "supplier",
    "country",
    "city",
    "purchase_date",
    "amount",
    "discount",
    "weight",
    "units",
    "unit_price",
    "contact_email",
  ]

  def unidad_invalida(x):
      if x.strip() in ["", "N/A"]:
          return False
      numero = pd.to_numeric(x, errors="coerce")

      return pd.isna(numero) or numero <= 0 or numero % 1 != 0

  reporte = {
    "row_count": len(df),
    "column_count": len(df.columns),
    "missing_required_columns": sorted([col for col in COLUMNAS_REQUERIDAS if col not in df.columns]),
    "unexpected_columns": sorted([col for col in df.columns if col not in COLUMNAS_REQUERIDAS]),
    "duplicate_row_count": int(df.duplicated().sum()),
    "duplicate_supplier_id_row_count": int(df.duplicated(subset=["supplier_id"], keep=False).sum()),
    "missing_value_count_by_column": {col: int(df[col].isin(["", "N/A"]).sum()) for col in df.columns},
    "invalid_email_count": int(sum(1 for x in df["contact_email"] if x not in ["", "N/A"] and not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", x))),
    "invalid_unit_count": int(df["units"].apply(unidad_invalida).sum()),
    "country_values": sorted(df["country"].unique().tolist()),
  }

  ruta_salida = Path(__file__).resolve().parent.parent / "submission" / "data_quality_report.json"
  ruta_salida.parent.mkdir(parents=True, exist_ok=True)
  with open(ruta_salida, "w") as f:
    json.dump(reporte, f)

  return reporte
