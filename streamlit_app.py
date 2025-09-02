import requests
from bs4 import BeautifulSoup
import pandas as pd
from supabase import create_client, Client

# Supabase setup
url = "https://your-supabase-url.supabase.co"
key = "your-supabase-api-key"
supabase: Client = create_client(url, key)

def fetch_tax_sale_data():
    response = requests.get("https://countytreasurer.org/tax-sales")
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Example: Extract table rows with parcel data
    rows = soup.select("table tr")
    data = []
    for row in rows[1:]:
        cols = row.find_all("td")
        if len(cols) >= 4:
            parcel = cols[0].text.strip()
            min_bid = float(cols[2].text.replace("$", "").replace(",", ""))
            sale_price = float(cols[3].text.replace("$", "").replace(",", ""))
            overage = sale_price - min_bid if sale_price > min_bid else 0
            data.append({"parcel": parcel, "min_bid": min_bid, "sale_price": sale_price, "overage": overage})
    
    return pd.DataFrame(data)

def store_in_supabase(df):
    for _, row in df.iterrows():
        supabase.table("riverside_overages").insert({
            "parcel": row["parcel"],
            "min_bid": row["min_bid"],
            "sale_price": row["sale_price"],
            "overage": row["overage"]
        }).execute()

# Run the pipeline
df = fetch_tax_sale_data()
store_in_supabase(df)
print("Overage data stored successfully.")
