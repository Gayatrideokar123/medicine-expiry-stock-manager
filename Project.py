from datetime import datetime
#function to check if medicine is expired
def is_expired(expiry_date_str):
    expiry_date=datetime.strptime(expiry_date_str,"%Y-%m-%d").date()
    today=datetime.today().date()
    return today>expiry_date
#dummy medicine data
medicines=[{"name":"paracetamol","expiry":"2025-08-10"},
           {"name":"cough syrup","expiry":"2025-12-5"},
           {"name":"freecold","expiry":"2025-04-8"}]
#test
for med in medicines:
    if is_expired(med["expiry"]):
        print(f"{med['name']}is expired.")
    else:
        print(f"{med['name']}is safe to use")
