import pandas as pd
from pathlib import Path

MESES = {
    "jan": "01", "feb": "02", "mar": "03",
    "apr": "04", "may": "05", "jun": "06",
    "jul": "07", "aug": "08", "sep": "09",
    "oct": "10", "nov": "11", "dec": "12"
}

def cargar_datasets():
    ruta = Path(__file__).resolve().parent.parent / "data"
    archivos = sorted(ruta.glob("bank-marketing-campaing-*.csv.gz"))

    df = pd.concat([pd.read_csv(archivo) for archivo in archivos], ignore_index=True)
    df = df.drop(columns=df.columns[0])

    return df

def limpiar_client(df):
    client = df[["client_id", "age", "job", "marital", "education", "credit_default", "mortgage"]].copy()

    client["job"] = (client["job"].str.replace(".", "", regex = False).str.replace("-", "_", regex = False))
    client["education"] = (client["education"].str.replace(".", "_", regex = False).replace("unknown", pd.NA))
    client["credit_default"] = (client["credit_default"] == "yes").astype(int)
    client["mortgage"] = (client["mortgage"] == "yes").astype(int)

    return client

def limpiar_campaign(df):
    campaign = df[["client_id", "number_contacts", "contact_duration", "previous_campaign_contacts", "previous_outcome", "campaign_outcome", "month", "day"]].copy()

    campaign["previous_outcome"] = (campaign["previous_outcome"] == "success").astype(int)
    campaign["campaign_outcome"] = (campaign["campaign_outcome"] == "yes").astype(int)

    fechas = (campaign["day"].astype(str).str.zfill(2)+ "-" + campaign["month"].str.lower().map(MESES) + "-2022")

    campaign["last_contact_date"] = pd.to_datetime(fechas, format="%d-%m-%Y").dt.strftime("%Y-%m-%d")
    campaign = campaign.drop(columns=["month", "day"])

    return campaign

def separar_economics(df):
    economics = df[["client_id", "cons_price_idx", "euribor_three_months"]].copy()

    return economics


def clean_campaign_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Los datos de una campaña de mercadeo bancario llegaron repartidos en diez
    archivos comprimidos, `data/bank-marketing-campaign-*.csv.gz`, con
    información mezclada del cliente, de la campaña y del contexto económico.
    Su tarea es leerlos directamente desde los archivos comprimidos, sin
    descomprimirlos a mano, y separarlos en tres tablas limpias.

    Guarde cada tabla como un CSV sin comprimir en `submission/`, sin el índice
    de Pandas y con las columnas en el orden indicado:

    1. `client.csv`: `client_id`, `age`, `job`, `marital`, `education`,
       `credit_default` y `mortgage`.
       - En `job`, elimine los puntos y cambie los guiones por guiones bajos.
       - En `education`, cambie los puntos por guiones bajos y deje el valor
         `unknown` como faltante.
       - En `credit_default` y `mortgage`, escriba 1 si el valor es `yes` y 0
         en cualquier otro caso.

    2. `campaign.csv`: `client_id`, `number_contacts`, `contact_duration`,
       `previous_campaign_contacts`, `previous_outcome`, `campaign_outcome` y
       `last_contact_date`.
       - En `previous_outcome`, escriba 1 si el valor es `success` y 0 en
         cualquier otro caso.
       - En `campaign_outcome`, escriba 1 si el valor es `yes` y 0 en
         cualquier otro caso.
       - Construya `last_contact_date` a partir de las columnas `month` y
         `day`, usando el año 2022 y el formato `AAAA-MM-DD`.

    3. `economics.csv`: `client_id`, `cons_price_idx` y
       `euribor_three_months`.

    La función también debe retornar las tres tablas, en el orden `client`,
    `campaign` y `economics`.

    Ejemplo del formato de `campaign.csv`:

        client_id,number_contacts,contact_duration,...,last_contact_date
        0,1,261,...,2022-05-13
        ...
    """
    df = cargar_datasets()

    client = limpiar_client(df)
    campaign = limpiar_campaign(df)
    economics = separar_economics(df)

    ruta_salida = (Path(__file__).resolve().parent.parent / "submission" )
  
    client.to_csv(ruta_salida / "client.csv", index=False)
    campaign.to_csv(ruta_salida / "campaign.csv", index=False)
    economics.to_csv(ruta_salida / "economics.csv", index=False)

    return client, campaign, economics
