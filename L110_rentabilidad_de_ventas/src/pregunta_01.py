import pandas as pd
from pathlib import Path

def calcular_resumen(df):
    lines = len(df)
    sales = df["Sales"].sum()
    profit = df["Profit"].sum()

    loss = df["Profit"] < 0

    return {
        "lines": lines,
        "sales": sales,
        "profit": profit,
        "profit_margin": profit / sales,
        "loss_lines": loss.sum(),
        "loss_line_rate": loss.sum() / lines,
        "lost_profit": -df.loc[loss, "Profit"].sum(),
    }

def clasificar_descuento(df):
    bins = [-float("inf"), 0, 0.05, 0.10, float("inf")]
    labels = ["0%", "1%-5%", "6%-10%", "más de 10%"]

    df = df.copy()

    df["discount_band"] = pd.cut(df["Discount"], bins=bins, labels=labels)

    return df

def crear_csv(df, nombre_archivo):
   df.to_csv(Path(__file__).resolve().parent.parent / "submission" / nombre_archivo, index=False)

def pregunta_01() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
   """
    Una cadena de suministros de oficina vende mucho, pero la gerencia
    sospecha que parte de esas ventas no deja utilidad. El archivo
    `data/superstore_orders.csv.gz` tiene una fila por línea de pedido, con
    el número de pedido (`Order ID`), las ventas (`Sales`), la utilidad
    (`Profit`), el descuento aplicado (`Discount`, como proporción), el
    segmento del cliente (`Customer Segment`) y la categoría del producto
    (`Product Category`). Una utilidad negativa significa que la línea se
    vendió con pérdida.

    Use estas definiciones:

    - Margen (`profit_margin`): utilidad sobre ventas.
    - Línea con pérdida: una línea cuya utilidad es negativa.
    - `loss_line_rate`: la proporción de líneas con pérdida.
    - `lost_profit`: la suma de las pérdidas de las líneas con pérdida,
      escrita como número positivo.
    - Rango de descuento (`discount_band`): `0%` si no hubo descuento,
      `1%-5%` si fue mayor que 0 y hasta 5 %, `6%-10%` si fue mayor que 5 % y
      hasta 10 %, y `más de 10%` en otro caso.

    Genere tres archivos en `submission/`, sin el índice de Pandas y con las
    columnas en el orden indicado:

    1. `profitability_summary.csv`, con una sola fila: `lines` (cantidad de
       líneas), `orders` (pedidos distintos), `sales`, `profit`,
       `profit_margin`, `loss_lines` (cantidad de líneas con pérdida),
       `loss_line_rate` y `lost_profit`.

    2. `discount_summary.csv`, con una fila por rango de descuento, en el
       orden en que se definieron arriba: `discount_band`, `lines`, `sales`,
       `profit`, `profit_margin`, `loss_line_rate` y `lost_profit`.

    3. `priority_segments.csv`, con los cinco segmentos segmento–categoría
       que más utilidad pierden: `Customer Segment`, `Product Category`,
       `lines`, `sales`, `profit`, `profit_margin` y `lost_profit`. Considere
       solamente segmentos con al menos 100 líneas y ordénelos por
       `lost_profit` de mayor a menor.

    La función también debe retornar las tres tablas, en el mismo orden.

    Ejemplo del formato de `discount_summary.csv`:

        discount_band,lines,sales,profit,profit_margin,loss_line_rate,...
        0%,166,170539.05,29472.3789,0.1728,0.488,...
        ...
   """
   ruta = Path(__file__).resolve().parent.parent / "data" / "superstore_orders.csv.gz"
   df = pd.read_csv(ruta, sep=";", decimal=",")

   resumen = calcular_resumen(df)
   orders = df["Order ID"].nunique()

   df = clasificar_descuento(df)

#creacion profitability_summary
   profitability_summary = pd.DataFrame([{
      "lines": resumen["lines"],
      "orders": orders,
      "sales": resumen["sales"],
      "profit": resumen["profit"],
      "profit_margin": resumen["profit_margin"],
      "loss_lines": resumen["loss_lines"],
      "loss_line_rate": resumen["loss_line_rate"],
      "lost_profit": resumen["lost_profit"]
   }])

# creacion discount_summary
   grupos = df.groupby("discount_band", observed=False)

   discount_summary = []

   for banda, grupo in grupos:
      resumen = calcular_resumen(grupo)

      discount_summary.append({
         "discount_band": banda,
         **{k: resumen[k] for k in ["lines", "sales", "profit", "profit_margin", "loss_line_rate", "lost_profit"]}
      })

   discount_summary = pd.DataFrame(discount_summary)

# creacion priority_segments
   grupos = df.groupby(["Customer Segment", "Product Category"])

   priority_segments = []

   for (segmento, categoria), grupo in grupos:
      resumen = calcular_resumen(grupo)

      priority_segments.append({
         "Customer Segment": segmento,
         "Product Category": categoria,
         **{k: resumen[k] for k in ["lines", "sales", "profit", "profit_margin", "lost_profit"]}
      })

   priority_segments = pd.DataFrame(priority_segments)
   priority_segments = priority_segments[priority_segments["lines"] >= 100]
   priority_segments = priority_segments.sort_values("lost_profit", ascending=False).head(5)

# creacion de los archivos csv
   crear_csv(profitability_summary, "profitability_summary.csv")
   crear_csv(discount_summary, "discount_summary.csv")
   crear_csv(priority_segments, "priority_segments.csv")

   return profitability_summary, discount_summary, priority_segments
