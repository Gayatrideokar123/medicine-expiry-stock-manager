import pandas as pd
from datetime import datetime, date, timedelta

# -----------------------------
# Constants
# -----------------------------
CSV_FILE = "medicine.csv"   # The CSV file where all medicine data is stored

# -----------------------------
# Core File Operations
# -----------------------------
def load_data():
    """Load medicine data from CSV into a Pandas DataFrame."""
    try:
        return pd.read_csv(CSV_FILE, parse_dates=["ExpiryDate"])
    except FileNotFoundError:
        # If no file exists yet, return empty DataFrame
        return pd.DataFrame(columns=["Name", "Quantity", "ExpiryDate"])


def save_data(df: pd.DataFrame):
    """Save the DataFrame back to CSV."""
    df.to_csv(CSV_FILE, index=False)


# -----------------------------
# Medicine CRUD Operations
# -----------------------------
def add_medicine(name: str, quantity: int, expiry_date: str):
    """
    Add a new medicine entry.
    expiry_date must be in YYYY-MM-DD format.
    """
    df = load_data()
    new_row = pd.DataFrame(
        {
            "Name": [name],
            "Quantity": [quantity],
            "ExpiryDate": [pd.to_datetime(expiry_date)],
        }
    )
    df = pd.concat([df, new_row], ignore_index=True)
    save_data(df)


def remove_medicine(name: str):
    """Remove a medicine by its name."""
    df = load_data()
    df = df[df["Name"] != name]
    save_data(df)


def update_quantity(name: str, new_quantity: int):
    """Update the quantity of a given medicine."""
    df = load_data()
    df.loc[df["Name"] == name, "Quantity"] = new_quantity
    save_data(df)


# -----------------------------
# Alerts (Green / Yellow / Red)
# -----------------------------
def get_alerts(low_stock_threshold: int = 10, expiring_days: int = 30):
    """
    Categorize medicines into green, yellow, red alerts:
      - Green: Safe (not expiring soon, stock is fine)
      - Yellow: Expiring soon (within expiring_days)
      - Red: Expired or critically low stock (<= 0)
    """

    df = load_data()
    if df.empty:
        return {"green": pd.DataFrame(), "yellow": pd.DataFrame(), "red": pd.DataFrame()}

    today = date.today()
    exp_limit = today + timedelta(days=expiring_days)

    # Red: expired or stock finished
    red = df[(df["ExpiryDate"].dt.date < today) | (df["Quantity"] <= 0)]

    # Yellow: expiring soon (but not expired)
    yellow = df[
        (df["ExpiryDate"].dt.date >= today) & (df["ExpiryDate"].dt.date <= exp_limit)
    ]

    # Green: safe (not expiring soon + good stock)
    green = df[
        (df["ExpiryDate"].dt.date > exp_limit) & (df["Quantity"] > low_stock_threshold)
    ]

    return {"green": green, "yellow": yellow, "red": red}


# -----------------------------
# Reporting (for exports)
# -----------------------------
def export_report(filename: str = "medicine_report.csv"):
    """Export current medicine stock into a CSV file report."""
    df = load_data()
    df.to_csv(filename, index=False)
    return filename


# -----------------------------
# Example (for testing only)
# -----------------------------
if __name__ == "__main__":
    # Demo usage
    add_medicine("Paracetamol", 20, "2025-12-01")
    add_medicine("Aspirin", 5, "2025-09-15")
    add_medicine("ExpiredDrug", 0, "2023-08-01")

    alerts = get_alerts()

    print("🟢 Safe Medicines:")
    print(alerts["green"])
    print("\n🟡 Expiring Soon:")
    print(alerts["yellow"])
    print("\n🔴 Critical Alerts:")
    print(alerts["red"])