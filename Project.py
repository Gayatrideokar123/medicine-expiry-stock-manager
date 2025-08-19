import pandas as pd
from datetime import datetime

CSV_FILE = "medicine.csv"

# Load data safely
def load_data():
    try:
        df = pd.read_csv(CSV_FILE)
        # Remove extra spaces / hidden chars
        df.columns = df.columns.str.strip()

        # Ensure required columns exist
        required_cols = ["Name", "Quantity", "Expiry_Date"]
        for col in required_cols:
            if col not in df.columns:
                df[col] = pd.Series(dtype="object")

        return df[required_cols]  # Return only correct columns

    except FileNotFoundError:
        df = pd.DataFrame(columns=["Name", "Quantity", "Expiry_Date"])
        df.to_csv(CSV_FILE, index=False)
        return df

# Save data
def save_data(df):
    df.to_csv(CSV_FILE, index=False)

# Add medicine
def add_medicine(name, quantity, expiry_date):
    df = load_data()
    new_data = pd.DataFrame([{
        "Name": name,
        "Quantity": int(quantity),
        "Expiry_Date": expiry_date
    }])
    df = pd.concat([df, new_data], ignore_index=True)
    save_data(df)

# Remove medicine
def remove_medicine(name):
    df = load_data()
    df = df[df["Name"] != name]
    save_data(df)

# Check expired
def check_expired():
    df = load_data()
    today = datetime.today().date()
    df["Expiry_Date"] = pd.to_datetime(df["Expiry_Date"], errors="coerce").dt.date
    expired = df[df["Expiry_Date"] < today]
    return expired

# Check low stock
def check_low_stock(threshold=5):
    df = load_data()
    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce").fillna(0).astype(int)
    low_stock = df[df["Quantity"] < threshold]
    return low_stock