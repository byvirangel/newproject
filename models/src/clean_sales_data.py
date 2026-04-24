from pathlib import Path
import pandas as pd
from rapidfuzz import process

# Project root
BASE_DIR = Path(__file__).resolve().parents[2]

# Input and output paths
input_path = BASE_DIR / "models/raw/messy_rain_jacket_sales_database.xlsx"
output_path = BASE_DIR / "models/processed/clean_sales_data.csv"

SHEET_NAME = "messy_sales_data"

VALID_CITIES = ["Sydney", "Melbourne", "Brisbane", "Perth"]


def correct_city(city):
    """
    Automatically correct city typos using fuzzy matching.

    Examples:
    - Sidney -> Sydney
    - Melbourn -> Melbourne
    - Brisban -> Brisbane
    - Perthh -> Perth
    """

    if pd.isna(city) or str(city).strip() == "":
        return "Unknown"

    city_clean = str(city).strip().title()

    match, score, _ = process.extractOne(city_clean, VALID_CITIES)

    if score >= 85:
        return match

    return "Unknown"


def clean_data():
    print("Reading raw file...")

    # We explicitly read the correct sheet: messy_sales_data.
    df = pd.read_excel(input_path, sheet_name=SHEET_NAME)

    print(f"Rows before cleaning: {len(df)}")

    # ---------------------------
    # 1. Clean date column
    # ---------------------------
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # Remove rows where date is not valid
    df = df.dropna(subset=["date"])

    # ---------------------------
    # 2. Clean and correct city names
    # ---------------------------
    df["city"] = df["city"].apply(correct_city)

    # ---------------------------
    # 3. Clean text columns
    # ---------------------------
    text_columns = ["store", "product", "sales_channel", "notes"]

    for col in text_columns:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

            # Replace "nan" text created from empty cells
            df[col] = df[col].replace("nan", "")

    # Standardise sales channel values
    if "sales_channel" in df.columns:
        df["sales_channel"] = (
            df["sales_channel"]
            .str.lower()
            .str.replace("-", " ", regex=False)
            .str.strip()
        )

        df["sales_channel"] = df["sales_channel"].replace({
            "in store": "In-store",
            "instore": "In-store",
            "in-store": "In-store",
            "online": "Online"
        })

    # ---------------------------
    # 4. Convert numeric fields
    # ---------------------------

    numeric_columns = ["sales_revenue_aud", "orders", "customers"]

    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # ---------------------------
    # 5. Handle missing values
    # ---------------------------

    # Revenue should not be guessed. If it is missing or invalid, set it to 0.
    df["sales_revenue_aud"] = df["sales_revenue_aud"].fillna(0)

    # Orders and customers are also key business metrics. For this first cleaning exercise, missing values are set to 0.
    df["orders"] = df["orders"].fillna(0)
    df["customers"] = df["customers"].fillna(0)

    # ---------------------------
    # 6. Basic validation
    # ---------------------------
    # Remove negative values if they exist.
    df = df[df["sales_revenue_aud"] >= 0]
    df = df[df["orders"] >= 0]
    df = df[df["customers"] >= 0]

    # Convert orders and customers to whole numbers
    df["orders"] = df["orders"].round().astype(int)
    df["customers"] = df["customers"].round().astype(int)

    # ---------------------------
    # 7. Remove duplicated rows
    # ---------------------------
    df = df.drop_duplicates()

    # ---------------------------
    # 8. Save cleaned data
    # ---------------------------
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"Rows after cleaning: {len(df)}")
    print("Saving cleaned data...")

    df.to_csv(output_path, index=False)

    print(f"Done! File saved at: {output_path}")


if __name__ == "__main__":
    clean_data()