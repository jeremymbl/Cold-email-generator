# BEFORE WE START: 
# 1. pip install python-dotenv
# 2. Create a .env file in the project root with lines like:
#       OPENAI_API_KEY=sk-xxxx
#       HUBSPOT_API_KEY=xxxx
# 3. Ensure .env is in .gitignore

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ================ OPENAI CONFIG ================ #
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", default="")

# ================ HUBSPOT CONFIG ================ #
HUBSPOT_API_KEY = os.getenv("HUBSPOT_API_KEY", default="")
HUBSPOT_BASE_URL = os.getenv("HUBSPOT_BASE_URL", default="")

# ================ FILE CONFIG ================ #
TAMTAM_EXCEL_FILE = "output-tamtam-lookalike-2024-11-13T18_42_33.xlsx"
OUTPUT_FILE = "generated_cold_emails.csv"