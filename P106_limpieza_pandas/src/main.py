from pathlib import Path

import pandas as pd

ACTIVITY_DIR = Path(__file__).resolve().parents[1]
INPUT_FILE = ACTIVITY_DIR / "data" / "ventas.csv"
OUTPUT_FILE = ACTIVITY_DIR / "submission" / "ventas.csv"

SUPPLIER_REPLACEMENTS = {
    "amazon web services colombia": "Amazon Web Services Colombia",
    "BANCOLOMBIA S.A.": "Bancolombia S.A.",
    "Cementos Argos SA": "Cementos Argos S.A.",
    "cementos argos s.a.": "Cementos Argos S.A.",
    "Corona SAS": "Corona S.A.S.",
    "Ecopetrol  S.A.": "Ecopetrol S.A.",
    "GOOGLE COLOMBIA LTDA.": "Google Colombia Ltda.",
    "Grupo  Éxito  S.A.": "Grupo Éxito S.A.",
    "IBM Colombia SAS.": "IBM Colombia S.A.S.",
    "ibm colombia s.a.s.": "IBM Colombia S.A.S.",
    "MICROSOFT COLOMBIA INC.": "Microsoft Colombia Inc.",
    "Nutresa SA": "Nutresa S.A.",
    "nutresa s.a.": "Nutresa S.A.",
    "oracle colombia ltda.": "Oracle Colombia Ltda.",
    "POSTOBÓN S.A.": "Postobon S.A.",
    "SAP Colombia SAS": "SAP Colombia S.A.S.",
    "Schneider  Electric": "Schneider Electric",
    "SIEMENS S.A.S.": "Siemens S.A.S.",
    "siemens s.a.s.": "Siemens S.A.S.",
    "Sura  S.A.": "Sura S.A.",
    "Telefónica  Colombia": "Telefónica Colombia",
}


def clean_column_names(df):
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )
    return df


def clean_supplier_column(df):
    replacements = {
        " ".join(key.split()).casefold(): value
        for key, value in SUPPLIER_REPLACEMENTS.items()
    }

    def clean_value(value):
        if pd.isna(value):
            return value

        normalized = " ".join(value.split())
        key = normalized.casefold()

        return replacements.get(key, normalized)

    df["supplier"] = df["supplier"].map(clean_value)
    return df

def clean_country_column(df):
    df["country"] = "COL"
    return df

def clean_city_column(df):
    replacements = {
        "bogotá": "Bogotá",
        "medellin": "Medellín",
        "medellín": "Medellín",
        "sopó": "Sopó",
        "tenjo": "Tenjo",
    }

    df["city"] = df["city"].apply(
        lambda value: replacements.get(
            value.strip().casefold(),
            value.strip()
        )
        if isinstance(value, str)
        else value
    )

    return df


def clean_purchase_date_column(df):
    def parse_date(value):
        if pd.isna(value):
            return value

        value = str(value).strip()
        if value[:4].isdigit() and len(value) >= 5 and value[4] in "-/.":
            date = pd.to_datetime(value, format="mixed", errors="raise", yearfirst=True)

        elif "-" in value and len(value.split("-")[-1]) == 2:
            date = pd.to_datetime(value, format="%d-%m-%y", errors="raise")

        elif "." in value:
            date = pd.to_datetime(value, format="%d.%m.%Y", errors="raise")

        elif "/" in value:
            parts = value.split("/")
            first, second, year = map(int, parts)

            if first > 12:
                date = pd.to_datetime(value, format="%d/%m/%Y", errors="raise")
            elif second > 12:
                date = pd.to_datetime(value, format="%m/%d/%Y", errors="raise")
            else:
                date = pd.to_datetime(value, format="%d/%m/%Y", errors="raise")
        else:
            raise ValueError(f"Fecha no reconocida: {value}")

        return date.strftime("%Y-%m-%d")

    df["purchase_date"] = df["purchase_date"].apply(parse_date)
    return df


def clean_amount_column(df):
    def clean_amount(value):
        if pd.isna(value):
            return pd.NA

        value = str(value).strip()
        value = value.replace("COP", "").replace("$", "").strip()

        if value.upper().endswith("K"):
            number = float(value[:-1].strip())
            return int(number * 1000)

        value = value.replace(",", "").replace(".", "")

        return int(value)

    df["amount"] = df["amount"].apply(clean_amount).astype("Int64")
    return df

def clean_discount_column(df):
    def clean_discount(value):
        if pd.isna(value):
            return pd.NA


        value = str(value).strip()

        # Si tiene %, convertir el porcentaje a decimal.
        if value.endswith("%"):
            return float(value[:-1].strip()) / 100
        
        number = float(value)
        if number > 1 and number <= 100:
            return number / 100

        if 0 <= number <= 1:
            return number

        raise ValueError(f"Descuento fuera de rango: {value}")

    df["discount"] = df["discount"].apply(clean_discount)
    return df



def clean_weight_column(df):
    def clean_weight(value):
        if pd.isna(value):
            return pd.NA

        value = str(value).strip().lower()

        if value.endswith("ton"):
            number = float(value.replace("ton", "").strip())
            return number * 1000

        if value.endswith("kg"):
            number = float(
                value.replace("kg", "").strip().replace(",", ".")
            )
            return number

        if value.endswith("g"):
            number = float(value.replace("g", "").strip())
            return number / 1000

        # Si no tiene unidad, asumimos que el valor está en kg.
        return float(value.replace(",", "."))

    df["weight"] = df["weight"].apply(clean_weight)
    return df


def clean_unit_price_column(df):
    def clean_unit_price(value):
        if pd.isna(value):
            return pd.NA

        value = str(value).strip()
        value = value.replace("$", "").replace(",", "")
        integer_part, decimal_part = value.rsplit(".", 1)
        integer_part = integer_part.replace(".", "")

        normalized = f"{integer_part}.{decimal_part}"
        return float(normalized)

    df["unit_price"] = df["unit_price"].apply(clean_unit_price)
    return df


def main():
    df = pd.read_csv(INPUT_FILE)

    df = clean_column_names(df)
    df = clean_supplier_column(df)
    df = clean_country_column(df)
    df = clean_city_column(df)
    df = clean_purchase_date_column(df)
    df = clean_amount_column(df)
    df = clean_discount_column(df)
    df = clean_weight_column(df)
    df = clean_unit_price_column(df)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False)

if __name__ == "__main__":
    main()