"""
data_loader.py

Responsible for loading data from Tamtam exports (Excel/CSV)
and merging it with CRM data from HubSpot, if available.
"""
import os
import requests
import pandas as pd
from config import (
    TAMTAM_EXCEL_FILE,
    HUBSPOT_API_KEY,
    HUBSPOT_BASE_URL
)


def load_tamtam_data() -> pd.DataFrame:
    """
    Loads the Tamtam lookalike data from an Excel file.
    Returns a pandas DataFrame with columns:
        - Company
        - Revenu
        - Countries
        - Strategy
        - Painpoints
        - Product use cases
    """
    # Read the Excel file
    df = pd.read_excel(TAMTAM_EXCEL_FILE)
    
    # Basic cleanup
    df.fillna("", inplace=True)
    return df


def load_hubspot_data() -> pd.DataFrame:
    """
    Demonstrates how to fetch data from HubSpot CRM using the API.
    Return a pandas DataFrame that you can merge with Tamtam data.
    
    This function is simplified. HubSpot has many endpoints, e.g. '/contacts/v1/contact'.
    You should adapt the endpoint & data you actually need.
    """
    """
    if not HUBSPOT_API_KEY or "YOUR_HUBSPOT_API_KEY_HERE" in HUBSPOT_API_KEY:
        # If user hasn't filled the key, just return an empty DataFrame
        # or log a message. We'll skip the real HubSpot call.
        print("HubSpot API Key not set. Skipping CRM data load.")
        return pd.DataFrame()
    
    try:
        url = f"{HUBSPOT_BASE_URL}/contacts/v1/lists/all/contacts/all"
        params = {
            "hapikey": HUBSPOT_API_KEY,
            "count": 100  # number of contacts to fetch
        }
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        # Extract only a minimal set of info for demonstration:
        # (In practice, you'd parse 'contacts' object more thoroughly)
        contacts = []
        for c in data.get("contacts", []):
            company_name = c.get("properties", {}).get("company", {}).get("value", "")
            domain = c.get("properties", {}).get("domain", {}).get("value", "")
            hs_contact_id = c.get("vid", "")
            contacts.append({
                "Company": company_name,
                "Domain": domain,
                "HS_Contact_ID": hs_contact_id
            })
        
        df = pd.DataFrame(contacts)
        return df
    
    except Exception as e:
        print(f"Error fetching HubSpot data: {e}")
        return pd.DataFrame()
    """
    print("HubSpot integration disabled. Returning empty DataFrame.")
    return pd.DataFrame()


def merge_data(tamtam_df: pd.DataFrame, hubspot_df: pd.DataFrame) -> pd.DataFrame:
    """
    Merges Tamtam data with HubSpot data on 'Company' or a relevant key.
    Returns a combined DataFrame.
    """
    if hubspot_df.empty:
        return tamtam_df
    
    # Merge on 'Company' column. Adjust if your actual data uses a different key.
    merged_df = pd.merge(tamtam_df, hubspot_df, on="Company", how="left")
    
    # Fill any new columns that are missing
    merged_df.fillna("", inplace=True)
    return merged_df