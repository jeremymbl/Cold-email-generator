import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", default="")

# useless for now
HUBSPOT_API_KEY = os.getenv("HUBSPOT_API_KEY", default="")
HUBSPOT_BASE_URL = os.getenv("HUBSPOT_BASE_URL", default="")

# files
TAMTAM_EXCEL_FILE = "output-tamtam-lookalike-2024-11-13T18_42_33.csv"
CRM_DATA_FILE = "crm_data.csv"
OUTPUT_FILE = "generated_cold_emails.csv"