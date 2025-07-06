from data_fetcher import fetch_historical_data, save_to_excel
from data_processor import combine_excel_files

# Fetch and save data
data = fetch_historical_data(
    start_date="29/12/2022",
    end_date="29/12/2022",
    exp_date="05/01/2023"
)
if data is not None:
    save_to_excel(data, "05-Jan-23.xlsx")

# Combine files
combine_excel_files(
    ["05-Jan-23.xlsx", "12-Jan-23.xlsx", "19-Jan-23.xlsx", "25-Jan-23.xlsx"],
    "Jan2023.xlsx"
)