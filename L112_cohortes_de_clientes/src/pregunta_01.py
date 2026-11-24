import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

def build_cohort_analysis() -> pd.DataFrame:
    """
    Una tienda quiere saber si sus clientes vuelven a comprar después de su
    primera compra. Para responder, agrupe a los clientes en cohortes según
    el mes de su primera compra y mida, mes a mes, qué proporción de cada
    cohorte vuelve a comprar. Use `data/sales.csv.gz`, que tiene una fila por
    orden con su cliente (`CustomerID`) y su fecha (`OrderDate`).

    Use estas definiciones:

    - `cohort_month`: el mes de la primera compra del cliente, escrito como
      `AAAA-MM`.
    - `period_index`: los meses transcurridos desde `cohort_month`; es 0 en el
      mes de la primera compra, 1 en el mes siguiente, y así sucesivamente.
    - `active_customers`: la cantidad de clientes distintos de la cohorte que
      compraron en ese período.
    - `cohort_size`: la cantidad de clientes de la cohorte, es decir, sus
      clientes activos en el período 0.
    - `retention_rate`: `active_customers` sobre `cohort_size`.

    Genere dos archivos en `submission/`:

    1. `cohort_retention.csv`, sin el índice de Pandas, con las columnas
       `cohort_month`, `period_index`, `active_customers`, `cohort_size` y
       `retention_rate`, y una fila por cada combinación cohorte–período
       observada, ordenadas por cohorte y período.

    2. `cohort_retention_heatmap.png`, un mapa de calor de `retention_rate`
       con una fila por cohorte (eje vertical) y una columna por período
       (eje horizontal). Muestre los valores como porcentajes. Los períodos
       que todavía no se pueden observar para una cohorte no significan
       retención cero: déjelos vacíos en el mapa.

    La función también debe retornar la tabla de retención.

    Ejemplo del formato de `cohort_retention.csv`:

        cohort_month,period_index,active_customers,cohort_size,retention_rate
        2022-01,0,100,100,1.0
        2022-01,1,26,100,0.26
        ...
    """
    ruta = Path(__file__).resolve().parent.parent / "data" / "sales.csv.gz"
    df = pd.read_csv(ruta, sep=",")

# organizar la fecha de compra
    df["OrderDate"] = pd.to_datetime(df["OrderDate"])
    df["purchase_month"] = df["OrderDate"].dt.to_period("M")

# calcular cohortes y retención
    df["cohort_month"] = df.groupby("CustomerID")["purchase_month"].transform("min")
    df["period_index"] = (df["purchase_month"].dt.year - df["cohort_month"].dt.year) * 12 + (df["purchase_month"].dt.month - df["cohort_month"].dt.month)
    df["active_customers"] = df.groupby(["cohort_month", "period_index"])["CustomerID"].transform("nunique")
    df["cohort_size"] = df.groupby("cohort_month")["CustomerID"].transform("nunique")
    df["retention_rate"] = df["active_customers"] / df["cohort_size"]

    cohort_retention = df[["cohort_month", "period_index", "active_customers", "cohort_size", "retention_rate"]].drop_duplicates().sort_values(by=["cohort_month", "period_index"])
    cohort_retention.to_csv(Path(__file__).resolve().parent.parent / "submission" / "cohort_retention.csv", index=False)

# generar mapa de calor
    heatmap_data = cohort_retention.pivot(index="cohort_month", columns="period_index", values="retention_rate")

    plt.figure(figsize=(12, 8))
    plt.title("Cohort Retention Rate Heatmap")
    plt.xlabel("Period Index")
    plt.ylabel("Cohort Month")
    plt.imshow(heatmap_data, cmap="plasma", aspect="auto")
    plt.colorbar(label="Retention Rate")
    plt.xticks(ticks=range(len(heatmap_data.columns)), labels=heatmap_data.columns)
    plt.yticks(ticks=range(len(heatmap_data.index)), labels=heatmap_data.index)

# agregar valores de retención al mapa de calor
    for i in range(len(heatmap_data.index)):
      for j in range(len(heatmap_data.columns)):
          valor = heatmap_data.iloc[i, j]

          if pd.notna(valor):
              plt.text(j, i, f"{valor:.1%}", ha="center", va="center")
    
    plt.savefig(Path(__file__).resolve().parent.parent / "submission" / "cohort_retention_heatmap.png")
    plt.close()

    return cohort_retention
