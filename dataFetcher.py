from datetime import datetime
import pandas as pd
import os
from dotenv import load_dotenv
from breeze_connect import BreezeConnect

# Load environment variables
load_dotenv()

# Initialize Breeze connection
breeze = BreezeConnect(api_key=os.getenv("API_KEY"))

def format_iso(date_str, time_str="07:00:00"):
    return f"{datetime.strptime(date_str, '%d/%m/%Y').date()}T{time_str}.000Z"

def fetch_historical_data(
    start_date, 
    end_date, 
    exp_date, 
    stock_code="NIFTY", 
    exchange_code="NFO", 
    interval="1minute", 
    product_type="options", 
    central_strike=18000
):

    strike_prices = [str(central_strike + i * 50) for i in range(-7, 7)]
    rights = ["call", "put"]
    all_data = []

    # Format dates
    iso_start = format_iso(start_date, "09:15:00")
    iso_end = format_iso(end_date, "15:30:00")
    iso_exp = format_iso(exp_date, "15:30:00")

    for strike_price in strike_prices:
        for right in rights:
            try:
                data = breeze.get_historical_data_v2(
                    interval=interval,
                    from_date=iso_start,
                    to_date=iso_end,
                    expiry_date=iso_exp,
                    stock_code=stock_code,
                    strike_price=strike_price,
                    product_type=product_type,
                    exchange_code=exchange_code,
                    right=right
                )

                if "Success" in data and isinstance(data["Success"], list):
                    df = pd.DataFrame(data["Success"])
                    all_data.append(df)
            except Exception as e:
                print(f"Error fetching {stock_code} {strike_price} {right}: {str(e)}")

    return pd.concat(all_data, ignore_index=True) if all_data else None

def save_to_excel(data, filename):
    if os.path.exists(filename):
        existing_data = pd.read_excel(filename, engine="openpyxl")
        combined_data = pd.concat([existing_data, data], ignore_index=True)
    else:
        combined_data = data

    combined_data.to_excel(filename, index=False, engine="openpyxl")
    print(f"Data successfully updated in {filename}")