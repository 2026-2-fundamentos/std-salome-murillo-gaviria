import pandas as pd
from pathlib import Path

def eliminar_indice(df):
  """Elimina la columna de índice que no pertenece a los datos."""
  df = df.drop(columns=df.columns[0])

  return df

def normalizar_texto(df):
  """Convierte los textos a minúsculas, elimina espacios y reemplaza guiones."""
  df = df.map(lambda x: x.lower().strip().replace("-", " ").strip() if isinstance(x, str) else x)

  return df

def limpiar_estrato(df):
  """Convierte estrato a números enteros."""
  df["estrato"] = df["estrato"].astype(int)

  return df

def limpiar_comuna(df):
  """Convierte comuna_ciudadano a enteros conservando los nulos."""
  df["comuna_ciudadano"] = pd.to_numeric(df["comuna_ciudadano"], errors="coerce").astype("Int64")

  return df

def limpiar_fecha(df):
  """Estandariza las fechas al formato AAAA-MM-DD."""
  fechas = df["fecha_de_beneficio"]

  fechas = pd.to_datetime(fechas, format="%d/%m/%Y", errors="coerce")

  for formato in ["%Y-%m-%d", "%Y/%m/%d"]:
    fechas = fechas.fillna(pd.to_datetime(df["fecha_de_beneficio"],format=formato,errors="coerce"))

  df["fecha_de_beneficio"] = fechas.dt.strftime("%Y-%m-%d")

  return df

def limpiar_monto(df):
  """Elimina símbolos y separadores del monto del crédito."""
  df["monto_del_credito"] = (df["monto_del_credito"].str.replace("$", "", regex=False).str.replace(" ", "", regex=False).str.replace(",", "", regex=False))

  df["monto_del_credito"] = pd.to_numeric(df["monto_del_credito"], errors="coerce").astype("Int64")

  return df

def eliminar_duplicados(df):
  """Elimina los registros duplicados."""
  df = df.drop_duplicates()

  return df

def eliminar_nulos(df):
  """Elimina registros incompletos, excepto por comuna_ciudadano."""
  columnas_evaluar = df.columns.drop("comuna_ciudadano")

  df = df.dropna(subset=columnas_evaluar)

  return df


def pregunta_01():
  """
    El archivo `data/solicitudes_de_credito.csv.gz` contiene las solicitudes de
    un programa de crédito, pero llegó sucio: tiene una columna de índice que
    no pertenece a los datos, registros duplicados, registros incompletos y
    valores que representan lo mismo escritos de formas distintas en los
    campos de texto, las fechas, el estrato y el monto.

    Su tarea es limpiarlo y guardar el resultado en
    `submission/solicitudes_de_credito.csv`, usando punto y coma (`;`) como
    separador y sin el índice de Pandas.

    El archivo limpio debe cumplir lo siguiente:

    - Contiene solamente las nueve columnas `sexo`, `tipo_de_emprendimiento`,
      `idea_negocio`, `barrio`, `estrato`, `comuna_ciudadano`,
      `fecha_de_beneficio`, `monto_del_credito` y `línea_credito`, en ese
      orden.
    - Los campos de texto están en minúsculas y sus palabras separadas por
      espacios.
    - `estrato` y `monto_del_credito` son números enteros, sin símbolos ni
      separadores de miles.
    - Todas las fechas de `fecha_de_beneficio` usan un mismo formato, por
      ejemplo `AAAA-MM-DD`.
    - No hay registros incompletos. La única excepción es
      `comuna_ciudadano`: sus valores faltantes son parte de los datos
      originales y deben conservarse.
    - No hay registros duplicados.

    Ejemplo del formato del archivo:

        sexo;tipo_de_emprendimiento;idea_negocio;barrio;estrato;...
        femenino;comercio;almacen de ropa en;los cerros el vergel;2;...
        ...
  """
  ruta = Path(__file__).resolve().parent.parent / "data" / "solicitudes_de_credito.csv.gz"
  df = pd.read_csv(ruta, dtype=str, sep=";")

  df = eliminar_indice(df)
  df = normalizar_texto(df)

  df = limpiar_estrato(df)
  df = limpiar_comuna(df)
  df = limpiar_fecha(df)
  df = limpiar_monto(df)

  df = eliminar_duplicados(df)
  df = eliminar_nulos(df)

  ruta_salida = (Path(__file__).resolve().parent.parent / "submission" / "solicitudes_de_credito.csv")
  
  df.to_csv(ruta_salida, sep=";", index=False)

  return df
