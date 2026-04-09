# import sys
# sys.path.append("/opt/spark")
import requests
from datetime import datetime

def get_rate(api_url: str) -> dict:
    """
    Fetch the current USD/MAD exchange rate from the given API URL.
    
    Args:
        api_url: The exchange rate API endpoint URL.
        
    Returns:
        dict with keys: rate, datetime, time_next_update
        
    Raises:
        requests.exceptions.RequestException: if the API call fails.
    """
    resp = requests.get(api_url)
    resp.raise_for_status()  # Raise an exception for HTTP errors
    data = resp.json()

    date_format = "%a, %d %b %Y %H:%M:%S %z"
    
    time_last_update_utc = datetime.strptime(data["time_last_update_utc"], date_format)
    formatted_last_date = time_last_update_utc.strftime("%Y-%m-%d %H:%M:%S")

    time_next_update_utc = datetime.strptime(data["time_next_update_utc"], date_format)
    formatted_next_date = time_next_update_utc.strftime("%Y-%m-%d %H:%M:%S")
    
    structure = {
        "base/target" : "USD/MAD",
        "rate" : data['rates']['MAD'],
        "datetime" : formatted_last_date,
        "time_next_update" : formatted_next_date
    }
    
    return structure
