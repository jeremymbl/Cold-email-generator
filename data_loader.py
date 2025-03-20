"""
data_loader.py

Responsible for loading data from Tamtam exports (Excel/CSV)
and merging it with CRM data from HubSpot, if available (right now, we're using crm_data.csv).
"""
import os
import requests
import pandas as pd
from config import (
    TAMTAM_EXCEL_FILE,
    CRM_DATA_FILE,
    HUBSPOT_API_KEY,
    HUBSPOT_BASE_URL
)


def load_tamtam_data() -> pd.DataFrame:
    df = pd.read_csv(TAMTAM_EXCEL_FILE, sep= ";")
    df.fillna("", inplace=True)
    return df


def load_hubspot_data() -> pd.DataFrame:
    file_path = CRM_DATA_FILE  
    df = pd.read_csv(file_path, sep=";", index_col=None)
    df.fillna("", inplace=True)
    return df


def merge_data(tamtam_df: pd.DataFrame, hubspot_df: pd.DataFrame) -> pd.DataFrame:
    if hubspot_df.empty:
        return tamtam_df
    crm_row = hubspot_df.iloc[0].to_dict()
    crm_row.pop("Company", None)
    for key, value in crm_row.items():
        tamtam_df[key] = value
    return tamtam_df
