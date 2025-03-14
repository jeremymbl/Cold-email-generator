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
        - Revenue
        - Countries
        - Strategy
        - Pain Points
        - Products & use cases
    """
    # Read the Excel file
    df = pd.read_csv(TAMTAM_EXCEL_FILE, sep= ";")

    # Basic cleanup
    df.fillna("", inplace=True)
    return df


def load_hubspot_data() -> pd.DataFrame:
    """
    Loads mock CRM data from a local CSV file named 'crm_data.csv'.
    This simulates fetching data from HubSpot.
    Assumes the file is tab-delimited and contains an extra index column.
    """
    file_path = "crm_data.csv"  # Make sure this file exists in your project directory

    if not os.path.exists(file_path):
        print(f"CRM data file not found at {file_path}. Returning empty DataFrame.")
        return pd.DataFrame()

    try:
        # Read the CSV using semicolon as separator and don't use any column as the index
        df = pd.read_csv(file_path, sep=";", index_col=None)
        # Basic cleanup: fill missing values with an empty string.
        df.fillna("", inplace=True)
        print("Loaded CRM data from crm_data.csv:")
        print(df.head())
        print("CRM Data columns:", df.columns.tolist())  # Debug print to verify column names
        return df
    except Exception as e:
        print(f"Error reading CRM data from {file_path}: {e}")
        return pd.DataFrame()


def merge_data(tamtam_df: pd.DataFrame, hubspot_df: pd.DataFrame) -> pd.DataFrame:
    """
    Merges Tamtam data with CRM data.
    Since the CRM data should be hardcoded (using the single CRM row for every company),
    we ignore the merge key and add the CRM data from the first row to every Tamtam row.
    """
    if hubspot_df.empty:
        return tamtam_df

    # Retrieve the hardcoded CRM row as a dictionary.
    crm_row = hubspot_df.iloc[0].to_dict()
    # Remove the 'Company' key to preserve the Tamtam company name.
    crm_row.pop("Company", None)

    # Add each CRM field to every row in the Tamtam dataframe.
    for key, value in crm_row.items():
        tamtam_df[key] = value

    return tamtam_df
